
import json, pathlib, subprocess, os
CONFIG = pathlib.Path.home() / ".config" / "racoogent" / "mcp_servers.json"

def load_servers():
    if not CONFIG.exists():
        return {}
    try:
        return json.loads(open(CONFIG).read())
    except:
        return {}

def save_servers(data):
    CONFIG.parent.mkdir(parents=True, exist_ok=True)
    open(CONFIG,"w").write(json.dumps(data, indent=2))

def add_server(name, command):
    servers = load_servers()
    servers[name] = {"command": command, "enabled": True}
    save_servers(servers)
    return servers

def list_servers():
    return load_servers()

def get_mcp_tools():
    # MCP는 실제로 stdio로 연결해서 tools/list 해야하지만, 지금은 스텁으로 등록
    # 나중에 pip install mcp 하면 실제 연결
    servers = load_servers()
    tools = []
    for name, cfg in servers.items():
        if not cfg.get("enabled"): continue
        # 각 MCP 서버가 제공하는 툴을 OpenAI function 형태로 변환한다고 가정
        tools.append({
            "type":"function",
            "function":{
                "name": f"mcp_{name}_call",
                "description": f"MCP server {name}: {cfg['command']} - tools will be dynamically fetched",
                "parameters": {"type":"object","properties":{"tool":{"type":"string"},"arguments":{"type":"object"}},"required":["tool"]}
            }
        })
    return tools
