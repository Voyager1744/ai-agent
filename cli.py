import structlog
import typer
from rich.console import Console
from core.agent import Agent
import asyncio

from tools.weather import WeatherTool, WeatherInput

app = typer.Typer()
console = Console()

log = structlog.get_logger(__name__)


@app.command()
def chat():
    console.print("[bold green]AI Agent with LLM[/bold green]")
    agent = Agent()

    while True:
        message = input("You: ")
        if message.lower() in {"exit", "quit"}:
            break
        reply = asyncio.run(agent.ask(message))
        console.print(f"[cyan]Agent:[/cyan] {reply}")


@app.command()
def weather(city: str):
    """Check weather for a city"""
    tool = WeatherTool()
    result = asyncio.run(tool.run(WeatherInput(city=city)))
    console.print(f"[cyan]Agent:[/cyan] {result}")


if __name__ == "__main__":
    app()
