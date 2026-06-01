from rich.console import Console
from rich.prompt import Prompt

console = Console()

while True:
    cmd = Prompt.ask("[bold green]junhyeok@pyterm[/bold green]:[blue]~[/blue]$")

    if cmd == "exit":
        break

    console.print(f"[yellow]입력한 명령어:[/yellow] {cmd}")