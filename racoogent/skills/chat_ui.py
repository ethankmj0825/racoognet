from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.box import ROUNDED

console = Console()

RACCOON = """[cyan]
 ⢀⣀⣤⣤⣤⣀⡀
⣠⡾⠋⠁ ⠈⠙⢷
⣰⠏ 🦝 RACOOGENT ⠹⣆ [bold white]local-first linux agent[/]
⣠⡾⠋ v0.1.0 ⠈⠙⢷⣄
⣰⠏ Your Linux, Your AI ⠹⣆
⠻⣆ ⣰⠟
  ⠙⠻⣦⣀⣀⣀⣤⠾⠋
[/]"""

def show_welcome(provider, model, mcp_count, skills):
    console.print(Panel(RACCOON, border_style="cyan", box=ROUNDED, padding=(1,2)))
    info = f"[bold]Provider:[/] {provider} [bold]Model:[/] {model or 'default'} [bold]MCP:[/] {mcp_count}"
    console.print(Panel(info, title="🚀 Ready", border_style="green", box=ROUNDED))

def print_agent(text):
    console.print(Panel(Markdown(text), title="🦝 racoogent", border_style="magenta", box=ROUNDED, padding=(1,2)))

def print_user(text):
    console.print(Panel(text, title="🧑 You", border_style="blue", box=ROUNDED, padding=(0,1)))

def input_box():
    # ANSI 코드 없이 깔끔하게
    console.print() # 한줄 띄우기
    console.print(Panel("", title="💬 You (Enter to send, /bye to exit)", border_style="blue", box=ROUNDED, height=3))
    # 그냥 바로 입력
    try:
        txt = console.input("[bold blue]❯ [/]")
    except EOFError:
        txt = "/bye"
    return txt

def print_tool(name, args):
    console.print(f"[dim]⚙ {name} {args}[/]")
