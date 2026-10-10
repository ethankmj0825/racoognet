import json
from pathlib import Path
SKILL_FILE = Path.home() / ".config" / "racoogent" / "skills.json"
SKILL_FILE.parent.mkdir(parents=True, exist_ok=True)
DEFAULTS = {"every-logs": False, "tui": False}
def load():
    if not SKILL_FILE.exists(): return DEFAULTS.copy()
    try:
        d=json.loads(SKILL_FILE.read_text())
        for k,v in DEFAULTS.items():
            if k not in d: d[k]=v
        return d
    except: return DEFAULTS.copy()
def save(d): SKILL_FILE.write_text(json.dumps(d,indent=2))
def is_enabled(n): return load().get(n,False)
def set_enabled(n,e): d=load(); d[n]=bool(e); save(d)
