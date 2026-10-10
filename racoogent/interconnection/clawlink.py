
import os, httpx, json, pathlib
CONFIG = pathlib.Path.home() / ".config" / "racoogent" / "clawlink.json"

def get_creds():
    return {
        "api_key": os.getenv("CLAWLINK_API_KEY"),
        "base_url": os.getenv("CLAWLINK_API_URL", "https://api.clawlink.ai/v1")
    }

def save_config(data):
    CONFIG.parent.mkdir(parents=True, exist_ok=True)
    open(CONFIG,"w").write(json.dumps(data, indent=2))

def list_skills():
    creds = get_creds()
    if not creds["api_key"]:
        return {"error": "CLAWLINK_API_KEY not set in.env"}
    try:
        r = httpx.get(f"{creds['base_url']}/skills", headers={"Authorization": f"Bearer {creds['api_key']}"}, timeout=10)
        return r.json()
    except Exception as e:
        return {"error": str(e), "hint": "Check CLAWLINK_API_URL"}

def call_skill(skill_name, args={}):
    creds = get_creds()
    try:
        r = httpx.post(f"{creds['base_url']}/skills/{skill_name}/call", headers={"Authorization": f"Bearer {creds['api_key']}"}, json=args, timeout=30)
        return r.json()
    except Exception as e:
        return {"error": str(e)}

def get_clawlink_tools():
    # 동적으로 skill을 tool로 변환
    data = list_skills()
    if "error" in data or "skills" not in data:
        return []
    tools = []
    for s in data.get("skills", []):
        tools.append({
            "type":"function",
            "function":{
                "name": f"clawlink_{s['name']}",
                "description": f"Clawlink skill: {s.get('description','')} (paid)",
                "parameters": s.get("parameters", {"type":"object","properties":{}})
            }
        })
    return tools
