import json
from pathlib import Path
from datetime import datetime
CHECKPOINT = Path.home() / ".config" / "racoogent" / "checkpoint.json"
def save_checkpoint(messages):
    CHECKPOINT.parent.mkdir(parents=True, exist_ok=True)
    data={"timestamp":datetime.now().isoformat(),"messages":messages[-20:]}
    CHECKPOINT.write_text(json.dumps(data,indent=2))
    print(f"💾 Checkpoint saved to {CHECKPOINT}")
def load_checkpoint():
    if not CHECKPOINT.exists(): return None
    return json.loads(CHECKPOINT.read_text())
