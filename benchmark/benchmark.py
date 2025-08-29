import requests
import time
import json
from tqdm import tqdm
import urllib3

# === CONFIGURATION ===
BASE_URL = "http://localhost:8080"
HEADERS = {
    "Authorization": "Bearer no-key",
    "Content-Type": "application/json"
}

MODEL_NAMES = [ 
    "qwen3-30b-coder-q4",
    "qwen3-30b-instruct-q4",
    "qwen3-30b-thinking-q4",
    "glm-4-32b-q4",
    "gpt-oss-20b"
]  

PROMPT = "Provide a detailed explanation of quantum computing in simple terms."
MAX_TOKENS = 1000
MAX_RETRIES = 10 
BACKOFF_FACTOR = 1.5  # Exponential backoff
TIMEOUT = 60  # Base timeout
WARMUP_ROUNDS = 2
BENCHMARK_ROUNDS = 5

# === HELPERS ===
def is_retryable_error(e):
    """Check if error is due to timeout or connection issue"""
    if isinstance(e, requests.exceptions.ReadTimeout):
        return True
    if isinstance(e, requests.exceptions.ConnectTimeout):
        return True
    if isinstance(e, requests.exceptions.ConnectionError):
        return True
    if "timeout" in str(e).lower() or "read timeout" in str(e).lower():
        return True
    return False

def retry_request(func, max_retries=MAX_RETRIES, backoff_factor=BACKOFF_FACTOR):
    """Retry a request with exponential backoff"""
    last_exception = None
    for attempt in range(max_retries):
        try:
            response = func()
            return response  # Success
        except Exception as e:
            last_exception = e
            if not is_retryable_error(e):
                break  # Don't retry non-retryable errors

            # Exponential backoff: wait 1s, 1.5s, 2.25s, etc.
            wait_time = backoff_factor ** attempt
            print(f"⚠️ Attempt {attempt + 1}/{max_retries} failed: {e}. Retrying in {wait_time:.1f}s...")
            time.sleep(wait_time)

    # If we get here, all retries failed
    raise last_exception

# === STEP 1: Auto-Discover Models ===
def get_available_models():
    print("🔍 Fetching list of available models...")
    try:
        resp = requests.get(f"{BASE_URL}/v1/models", timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            models = [m["id"] for m in data["data"]]
            print(f"✅ Found {len(models)} models:")
            for model in models:
                print(f"  - {model}")
            return models
        else:
            print(f"❌ Failed to fetch models: {resp.status_code} - {resp.text}")
            return []
    except Exception as e:
        print(f"⚠️ Error connecting to /v1/models: {e}")
        return []

# === STEP 2: Benchmark One Model (with retries) ===
def benchmark(model_name, prompt, rounds):
    print(f"\n🔄 Loading model: {model_name}")

    # Use retry wrapper for each request
    def make_request():
        resp = requests.post(
            f"{BASE_URL}/v1/chat/completions",
            json={
                "model": model_name,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": MAX_TOKENS,
                "stream": True
            },
            headers=HEADERS,
            stream=True,
            timeout=TIMEOUT
        )
        return resp

    results = []

    for _ in tqdm(range(rounds), desc="Benchmarking"):
        # ✅ Define start_time HERE — after retry logic
        start_time = time.time()
        first_token_time = None
        total_tokens = 0
        last_exception = None

        # Retry the entire request
        try:
            resp = retry_request(make_request, max_retries=MAX_RETRIES, backoff_factor=BACKOFF_FACTOR)

            # Now process streaming
            for line in resp.iter_lines():
                if line:
                    if line.startswith(b"data: "):
                        line = line[6:]
                    elif line.startswith(b"data"):
                        line = line[5:]
                    try:
                        data = json.loads(line.decode("utf-8"))
                    except:
                        continue

                    if "choices" in data:
                        for choice in data["choices"]:
                            if "delta" in choice and "content" in choice["delta"]:
                                if first_token_time is None:
                                    first_token_time = time.time()
                                total_tokens += 1

            total_time = time.time() - start_time
            ttft = first_token_time - start_time if first_token_time else float('inf')
            tps = total_tokens / total_time if total_time > 0 else 0

            results.append({
                "ttft": ttft,
                "tps": tps,
                "total_tokens": total_tokens,
                "total_time": total_time
            })

            resp.close()

        except Exception as e:
            print(f"❌ Error with {model_name}: {e}")
            results.append({
                "ttft": float('inf'),
                "tps": 0,
                "total_tokens": 0,
                "total_time": 0
            })

    # Aggregate results
    avg_ttft = sum(r["ttft"] for r in results) / len(results)
    avg_tps = sum(r["tps"] for r in results) / len(results)
    total_tokens = sum(r["total_tokens"] for r in results)
    total_time = sum(r["total_time"] for r in results)

    print(f"✅ Summary for {model_name}:")
    print(f"  Average TTFT: {avg_ttft:.3f}s")
    print(f"  Average TPS: {avg_tps:.2f}")
    print(f"  Total tokens: {total_tokens}")
    print(f"  Total time: {total_time:.2f}s")

    return {
        "model": model_name,
        "avg_ttft": avg_ttft,
        "avg_tps": avg_tps,
        "total_tokens": total_tokens,
        "total_time": total_time
    }

# === STEP 3: Run Benchmark on All Models ===
def main():
    print("🚀 Starting benchmark...")

    # Auto-discover models
    MODEL_NAMES = get_available_models()
    if not MODEL_NAMES:
        print("❌ No models available. Exiting.")
        return

    # Run benchmark
    all_results = []
    for model in MODEL_NAMES:
        print(f"\n{'='*60}")
        result = benchmark(model, PROMPT, BENCHMARK_ROUNDS)
        all_results.append(result)

    # Save results
    with open("benchmark_results.json", "w") as f:
        for result in all_results:
            f.write(json.dumps(result) + "\n")

    print("✅ ✅ All benchmarks complete!")
    print("✅ Results saved to benchmark_results.jsonl")

# === RUN IT ===
if __name__ == "__main__":
    main()
