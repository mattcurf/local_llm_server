# CLAUDE.md

## vLLM Server

### Qwen3-Coder Tool Calling

**Critical:** Use `qwen3_coder` parser for Qwen3-Coder models, NOT `hermes`:
```yaml
command:
  - --enable-auto-tool-choice
  - --tool-call-parser=qwen3_coder
```

Reference: https://docs.vllm.ai/projects/recipes/en/latest/Qwen/Qwen3-Coder-480B-A35B.html

### Recommended vLLM Flags for Qwen3-Coder
```yaml
- --model=<qwen3-coder-model>
- --enable-auto-tool-choice
- --tool-call-parser=qwen3_coder
- --enable-chunked-prefill
- --enable-prefix-caching
- --kv-cache-dtype=fp8
```

## claude-code-router

### Use Official Docker Image

Use `musistudio/claude-code-router:latest` instead of manual npm install:
```yaml
claude-code-router:
  image: musistudio/claude-code-router:latest
  volumes:
    - ./claude-code-router:/root/.claude-code-router
  environment:
    - OPENROUTER_API_KEY=${OPENROUTER_API_KEY}
```

The official image uses PM2 for process supervision - no custom startup scripts needed.

Reference: https://musistudio.github.io/claude-code-router/docs/server/deployment

### Volume Mount Path

The image expects config at `/root/.claude-code-router/`, NOT `/app/.claude-code-router/`:
```yaml
volumes:
  - ./claude-code-router:/root/.claude-code-router
```

### Custom Router Path

Must be absolute path inside container:
```json
{
  "CUSTOM_ROUTER_PATH": "/root/.claude-code-router/custom-router.js"
}
```

### Environment Variables

Environment variables are baked at container **creation** time. If you change `.env`:
```bash
docker compose up -d --force-recreate claude-code-router
```

A simple `docker compose restart` will NOT pick up new env var values.

### Common Issues

**ECONNRESET errors:**
- Check if PM2 process is running: `docker top claude-code-router`
- Should see `pm2-runtime` and `node /app/packages/server/dist/index.js`

**401 "No cookie auth credentials found" from OpenRouter:**
- `OPENROUTER_API_KEY` not reaching container
- Check: `docker exec claude-code-router sh -c 'echo $OPENROUTER_API_KEY'`
- Fix: Recreate container with `--force-recreate`

**Custom router not loading:**
- Check logs for: `failed to load custom router: Cannot find module`
- Fix: Use absolute path `/root/.claude-code-router/custom-router.js`

### Health Check

```yaml
healthcheck:
  test: ["CMD-SHELL", "curl -sf http://localhost:3456/health || exit 1"]
  interval: 30s
  timeout: 5s
  retries: 3
  start_period: 30s
```

### Debugging

Check router logs:
```bash
tail -f ./claude-code-router/logs/ccr-*.log
```

Check if providers registered:
```bash
grep "provider registered" ./claude-code-router/logs/ccr-*.log
```
