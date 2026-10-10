from pathlib import Path
import os
try:
    import httpx
except ImportError:
    httpx = None

PROVIDERS = {
    "1": {"id": "openai", "name": "OpenAI API", "key": "OPENAI_API_KEY", "url": "https://platform.openai.com/api-keys"},
    "2": {"id": "llama", "name": "Llama API (Ollama Cloud / Together.ai)", "key": "LLAMA_API_KEY", "url": "https://ollama.com/settings/keys"},
    "3": {"id": "gemini", "name": "Gemini API", "key": "GEMINI_API_KEY", "url": "https://aistudio.google.com/apikey"},
    "4": {"id": "deepseek", "name": "DeepSeek API", "key": "DEEPSEEK_API_KEY", "url": "https://platform.deepseek.com/api_keys"},
    "5": {"id": "alibaba", "name": "Alibaba Cloud API", "key": "ALIBABA_API_KEY", "url": "https://modelstudio.console.alibabacloud.com/"},
}

def fetch_ollama_models(base_url, api_key):
    if not httpx:
        return []
    models = []
    try:
        url = base_url.rstrip("/") + "/models"
        r = httpx.get(url, headers={"Authorization": f"Bearer {api_key}"}, timeout=10)
        if r.status_code == 200:
            data = r.json()
            if "data" in data:
                models = [m["id"] for m in data["data"]]
            elif "models" in data:
                models = [m["name"] for m in data["models"]]
        if not models:
            r2 = httpx.get(base_url.rstrip("/").replace("/v1","") + "/api/tags", headers={"Authorization": f"Bearer {api_key}"}, timeout=10)
            if r2.status_code == 200:
                models = [m["name"] for m in r2.json().get("models",[])]
    except Exception as e:
        print(f"(Failed to fetch models: {e})")
    return sorted(models)

def run():
    print("\n=== RacooGent First Setup ===\n")
    print("Select LLM API")
    for num, p in PROVIDERS.items():
        print(f"({num}) {p['name']}")
    choice = input("\nEnter number (e.g. 2 or 1,2,3): > ").strip()
    env_path = Path(".env")
    env_data = {}
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                if "=" in line and not line.startswith("#"):
                    k,v = line.strip().split("=",1)
                    env_data[k]=v
    for c in [x.strip() for x in choice.split(",")]:
        if c not in PROVIDERS: continue
        p = PROVIDERS[c]
        print(f"\n[{p['id']}] Get key from: {p['url']}")
        api_key = input(f"[{p['id']}] API Key: > ").strip()
        if not api_key: continue
        env_data[p['key']] = api_key
        if p['id'] == 'llama':
            base = input(f"[{p['id']}] Base URL [https://ollama.com/v1]: > ").strip()
            base = base if base else 'https://ollama.com/v1'
            env_data['LLAMA_BASE_URL'] = base
            print(f"[{p['id']}] 모델 목록 불러오는 중... ({base})")
            models = fetch_ollama_models(base, api_key)
            if models:
                print(f"\n[{p['id']}] Models available ({len(models)}개):")
                for i, m in enumerate(models, 1):
                    print(f"({i}) {m}")
                sel = input(f"\nSelect (1-{len(models)}) or 직접 입력: > ").strip()
                if sel.isdigit() and 1 <= int(sel) <= len(models):
                    env_data['LLAMA_MODEL'] = models[int(sel)-1]
                elif sel:
                    env_data['LLAMA_MODEL'] = sel
                else:
                    env_data['LLAMA_MODEL'] = models[0]
            else:
                model = input(f"[{p['id']}] Model [gpt-oss:20b]: > ").strip()
                env_data['LLAMA_MODEL'] = model if model else 'gpt-oss:20b'
    with open(env_path, 'w') as f:
        for k,v in env_data.items():
            f.write(f"{k}={v}\n")
    print("\n.env saved! ✅")
