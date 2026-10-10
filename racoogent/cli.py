import typer, os, httpx, json
from pathlib import Path
from dotenv import load_dotenv
from racoogent.config import load_config
from racoogent.interconnection import InterconnectionService
from racoogent.llm.factory import get_llm
from racoogent.commands.first_setup import run as run_first_setup
load_dotenv()
app = typer.Typer()

def _maybe_show_tui():
    import sys
    if "skill" in sys.argv: return
    try:
        from racoogent.skills.manager import is_enabled
        from racoogent.skills.tui import show as show_tui
        if is_enabled("tui"): show_tui()
    except: pass

@app.callback()
def _root(): _maybe_show_tui()

def detect_provider():
    if os.getenv("LLAMA_API_KEY"): return "llama"
    if os.getenv("OPENAI_API_KEY"): return "openai"
    if os.getenv("GEMINI_API_KEY"): return "gemini"
    return "ollama"

def update_env_model(m):
    p=Path(".env"); lines=p.read_text().splitlines() if p.exists() else []; new=[]; found=False
    for l in lines:
        if l.startswith("LLAMA_MODEL="): new.append(f"LLAMA_MODEL={m}"); found=True
        else: new.append(l)
    if not found: new.append(f"LLAMA_MODEL={m}")
    p.write_text("\n".join(new)+"\n")

def fetch_models():
    base=os.getenv("LLAMA_BASE_URL","https://ollama.com/v1"); key=os.getenv("LLAMA_API_KEY")
    if not key: return []
    try:
        r=httpx.get(base.rstrip("/")+"/models", headers={"Authorization": f"Bearer {key}"}, timeout=10)
        if r.status_code==200 and "data" in r.json(): return [x["id"] for x in r.json()["data"]]
    except: pass
    return []

@app.command()
def first_setup(): run_first_setup()
@app.command()
def models():
    ms=fetch_models(); curr=os.getenv("LLAMA_MODEL")
    for i,m in enumerate(ms,1): print(f"({i}) {m}{' <-- current' if m==curr else ''}")
@app.command()
def use(model: str): update_env_model(model); print(f"✅ {model}")
@app.command()
def mcp(action: str=typer.Argument(...), name: str=typer.Argument(None), command: str=typer.Argument(None), token_key: str=typer.Argument(None)):
    cfg=Path.home()/".config"/"racoogent"/"mcp_servers.json"; cfg.parent.mkdir(parents=True,exist_ok=True)
    if not cfg.exists(): cfg.write_text("{}")
    data=json.loads(cfg.read_text())
    if action=="list":
        if not data: print("No MCP")
        else:
            for k,v in data.items(): print(f"- {k}: {v.get('command') if isinstance(v,dict) else v}")
    elif action=="add":
        if not name or not command: print('add <name> "<cmd>"'); return
        if token_key and "=" in token_key: k,v=token_key.split("=",1); data[name]={"command":command,"env":{k:v}}
        else: data[name]=command
        cfg.write_text(json.dumps(data,indent=2)); print(f"✅ {name}")
    elif action=="add-token":
        if "=" not in token_key: return
        k,v=token_key.split("=",1); ex=data.get(name,""); ex={"command":ex,"env":{}} if isinstance(ex,str) else ex; ex.setdefault("env",{})[k]=v; data[name]=ex; cfg.write_text(json.dumps(data,indent=2)); print(f"✅ {k}")
    elif action=="remove": data.pop(name,None); cfg.write_text(json.dumps(data,indent=2))

@app.command()
def skill(name: str=typer.Argument(...), action: str=typer.Argument("status"), value: str=typer.Argument(None)):
    from racoogent.skills.manager import set_enabled, is_enabled
    from racoogent.skills.restoration import CHECKPOINT
    import subprocess, json
    n=name.lower()
    def to_bool(s): return s.lower() in ["true","1","on","yes"] if s else True
    if n in ["tui","every-logs"]:
        if n=="every-logs" and action=="view":
            p=Path.home()/".config"/"racoogent"/"execution.log"
            if p.exists(): print(p.read_text()[-2000:])
            else: print("No logs"); return
        if action=="enable":
            b=False if (value and value.lower() in ["false","0","off","no"]) else (to_bool(value) if value else True)
        elif action=="disable": b=False
        elif action in ["true","on"]: b=True
        elif action in ["false","off"]: b=False
        elif action=="status": print(f"{n}: {is_enabled(n)}"); return
        else: print("usage"); return
        set_enabled(n,b); print(f"{'✅' if b else '🛑'} {n} {'enabled' if b else 'disabled'}")
    elif n in ["stop-and-restoration","stop"]:
        if CHECKPOINT.exists(): print(json.loads(CHECKPOINT.read_text())["timestamp"])
        else: print("No checkpoint")

@app.command()
def chat(provider: str=None, model: str=None):
    from racoogent.skills.manager import is_enabled, load as load_skills
    from racoogent.skills.restoration import save_checkpoint, CHECKPOINT
    from racoogent.skills.chat_ui import console, show_welcome, print_agent, print_user, input_box, print_tool
    import sys, json
    restored=None
    if CHECKPOINT.exists():
        d=json.loads(CHECKPOINT.read_text())
        console.print(f"[yellow]💾 checkpoint {d['timestamp']}[/]")
        if console.input("Restore? [y/N]: ").lower()=="y": restored=d["messages"]
        else: CHECKPOINT.unlink(missing_ok=True)

    if provider is None: provider=detect_provider()
    final=model or os.getenv("LLAMA_MODEL")

    mcp_path=Path.home()/".config"/"racoogent"/"mcp_servers.json"
    mcp_count=len(json.loads(mcp_path.read_text())) if mcp_path.exists() else 0
    skills_enabled=[k for k,v in load_skills().items() if v]
    show_welcome(provider, final, mcp_count, skills_enabled)

    # ★ racoogent가 먼저 HI!
    print_agent("HI! 👋 I'm **racoogent** - your local-first Linux agent! 🦝\n\nWhat can I help you with today?")

    config=load_config(); ic=InterconnectionService(config); llm=get_llm(provider, final)
    messages=restored if restored else [{"role":"system","content":"You are racoogent, friendly raccoon agent"}]

    orig=ic.execute_tool
    def logged(a,b):
        if is_enabled("every-logs"): print_tool(a,b)
        return orig(a,b)
    ic.execute_tool=logged

    try:
        while True:
            # ★ 네가 치는건 밑에 네모 박스
            u = input_box()
            if not u: continue
            if u.strip()=="/bye": console.print("[dim]Bye! 👋[/]"); break
            if u.strip()=="/clear":
                console.clear(); show_welcome(provider, final, mcp_count, skills_enabled)
                print_agent("HI! 👋 Ready again!")
                continue

            # 네가 친건 파란 박스에
            print_user(u)
            messages.append({"role":"user","content":u})

            with console.status("[magenta]racoogent is typing...[/]", spinner="dots"):
                resp=llm.chat(messages, tools=ic.get_tool_definitions())

            # 얘가 말한건 마젠타 박스에
            print_agent(resp["content"])

            while resp.get("tool_calls"):
                for tc in resp["tool_calls"]:
                    print_tool(tc["name"], tc["arguments"])
                    out=ic.execute_tool(tc["name"], tc["arguments"])
                    messages.append({"role":"tool","tool_call_id":tc["id"],"content":str(out)})
                with console.status("[yellow]Executing tools...[/]", spinner="bouncingBar"):
                    resp=llm.chat(messages, tools=ic.get_tool_definitions())
                print_agent(resp["content"])
            messages.append({"role":"assistant","content":resp["content"]})

    except KeyboardInterrupt:
        console.print("\n[yellow]⏸️ Saving...[/]"); save_checkpoint(messages); sys.exit(0)

if __name__=="__main__": app()
