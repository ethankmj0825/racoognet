
from.sandbox import Sandbox
from.tools import TOOLS
from.mcp_manager import get_mcp_tools
from.clawlink import get_clawlink_tools, call_skill
import os

class InterconnectionService:
    def __init__(self, config):
        ic = config.get("interconnection", {})
        self.sandbox = Sandbox(ic.get("sandbox_dir","~/racoogent_sandbox"))
        self.base_tools = TOOLS

    def get_tool_definitions(self):
        tools = list(self.base_tools)
        try:
            tools.extend(get_mcp_tools())
        except Exception as e:
            print(f"[mcp] load fail: {e}")
        try:
            tools.extend(get_clawlink_tools())
        except Exception as e:
            print(f"[clawlink] load fail: {e}")
        return tools

    def execute_tool(self, name, args):
        # 기존 툴
        if name=="run_shell":
            return self.sandbox.run_shell(args.get("command",""))
        if name=="read_file":
            return self.sandbox.read_file(args.get("path",""))
        # MCP
        if name.startswith("mcp_"):
            return f"[MCP] {name} called with {args} - 실제 MCP 연결은 npx 실행 필요. pip install mcp 후 확장 예정"
        # Clawlink
        if name.startswith("clawlink_"):
            skill = name.replace("clawlink_","")
            return call_skill(skill, args)
        return f"Unknown tool {name}"

    # 예전 이름 호환
    def execute(self, name, args):
        return self.execute_tool(name, args)
