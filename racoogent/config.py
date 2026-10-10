import os, yaml, pathlib
from dotenv import load_dotenv
load_dotenv()
CONFIG_PATH = pathlib.Path.home() / ".config" / "racoogent" / "config.yaml"
DEFAULT_CONFIG = {
    "llm": {"provider": "openai","model":"gpt-4o-mini"},
    "interconnection": {"allow_shell": True, "allow_file_write": True, "sandbox_dir": "~/racoogent_sandbox"}
}
def load_config():
    if CONFIG_PATH.exists():
        return yaml.safe_load(open(CONFIG_PATH))
    return DEFAULT_CONFIG
def init_config():
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not CONFIG_PATH.exists():
        yaml.dump(DEFAULT_CONFIG, open(CONFIG_PATH,"w"), allow_unicode=True)
        print(f"Config created at {CONFIG_PATH}")
