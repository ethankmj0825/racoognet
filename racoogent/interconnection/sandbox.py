import pathlib, subprocess
class Sandbox:
    def __init__(self, sandbox_dir="~/racoogent_sandbox", allow_shell=True, allow_write=True):
        self.root = pathlib.Path(sandbox_dir).expanduser()
        self.root.mkdir(parents=True, exist_ok=True)
        self.allow_shell = allow_shell
    def run_shell(self, command: str) -> str:
        if "rm -rf /" in command: return "Blocked"
        try:
            r = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=15)
            return r.stdout + r.stderr
        except Exception as e: return str(e)
    def read_file(self, path: str) -> str:
        try: return pathlib.Path(path).expanduser().read_text()[:10000]
        except Exception as e: return str(e)
