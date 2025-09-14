# =========================
# Builder: compile llama.cpp with CUDA (architectures=all)
# =========================
FROM pytorch/pytorch:2.7.1-cuda12.8-cudnn9-devel AS builder

ARG LLAMA_CPP_TAG=master
ARG MAKE_JOBS=8

ENV DEBIAN_FRONTEND=noninteractive \
    TZ=America/Los_Angeles \
    PIP_ROOT_USER_ACTION=ignore \
    HF_HUB_ENABLE_HF_TRANSFER=1

RUN apt-get update && apt-get install -y --no-install-recommends \
      git ca-certificates build-essential cmake ninja-build pkg-config curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt
RUN git clone https://github.com/ggerganov/llama.cpp.git && \
    cd llama.cpp && git fetch --all --tags && git checkout "${LLAMA_CPP_TAG}"

# Build with CUDA and *all* architectures; copy all produced binaries
RUN cd /opt/llama.cpp && \
    cmake -S . -B build -G Ninja \
      -DCMAKE_BUILD_TYPE=Release \
      -DBUILD_SHARED_LIBS=OFF \ 
      -DGGML_STATIC=ON \ 
      -DGGML_CUDA=ON \
      -DGGML_CUDA_F16=ON \
      -DGGML_CUDA_DMMV_X=64 \
      -DGGML_CUDA_MMV_Y=1 \
      -DGGML_CUDA_ARCHITECTURES=all \
      -DLLAMA_CURL=OFF \
    && cmake --build build -j "${MAKE_JOBS}" \
    && mkdir -p /opt/llama.bin && cp -v build/bin/* /opt/llama.bin/


# =========================
# Build llama-swap from source (Go 1.23 + UI) and normalize artifact
# =========================
FROM golang:1.23-bookworm AS swapbuild
ENV CGO_ENABLED=0 GOFLAGS="-trimpath"
WORKDIR /src

# UI deps + make-based build
RUN apt-get update && apt-get install -y --no-install-recommends \
      git ca-certificates make nodejs npm \
    && rm -rf /var/lib/apt/lists/* \
    && npm -g install pnpm@9

# Clone and build (emits into build/…); then normalize to /out/llama-swap
RUN git clone https://github.com/mostlygeek/llama-swap.git . \
 && make clean all \
 && set -eux; \
    mkdir -p /out; \
    bin="$(find build -maxdepth 1 -type f -perm -111 -name 'llama-swap*' | head -n1)"; \
    test -n "$bin"; \
    install -Dm755 "$bin" /out/llama-swap


# =========================
# Runtime: CUDA + llama.cpp bins + llama-swap
# =========================
FROM pytorch/pytorch:2.7.1-cuda12.8-cudnn9-runtime

ENV DEBIAN_FRONTEND=noninteractive \
    TZ=America/Los_Angeles \
    PIP_ROOT_USER_ACTION=ignore \
    HF_HUB_ENABLE_HF_TRANSFER=1

RUN apt-get update && apt-get install -y --no-install-recommends \
      git ca-certificates wget curl tini bash libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# llama.cpp binaries
COPY --from=builder   /opt/llama.bin/      /usr/local/bin/

# llama-swap (normalized path)
COPY --from=swapbuild /out/llama-swap      /usr/local/bin/llama-swap

# Working directory for configs/models/scripts
WORKDIR /project

# Run wrapper: requires a mounted /project/config.yaml
COPY --chown=root:root <<'BASH' /project/scripts/run.sh
#!/usr/bin/env bash
set -euo pipefail
CONFIG="/project/config.yaml"
: "${LISTEN_ADDR:=0.0.0.0:8080}"

if [[ ! -f "$CONFIG" ]]; then
  echo "ERROR: $CONFIG not found. Mount your config file, e.g.:"
  echo "  docker run ... -v \$(pwd)/config.yaml:/project/config.yaml ..."
  exit 1
fi

exec /usr/bin/tini -- /usr/local/bin/llama-swap --config "$CONFIG" --listen "${LISTEN_ADDR}"
BASH
RUN chmod +x /project/scripts/run.sh

# Simple healthcheck for the UI
HEALTHCHECK --interval=30s --timeout=5s --retries=5 \
  CMD curl -fsS http://127.0.0.1:8080/ui >/dev/null || exit 1

EXPOSE 8080
ENTRYPOINT ["/bin/bash", "/project/scripts/run.sh"]

