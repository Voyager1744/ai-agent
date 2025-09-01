import structlog
import typer
from rich.console import Console
import logging

import asyncio
from tools.weather import WeatherTool, WeatherInput

app = typer.Typer()
console = Console()

log = structlog.get_logger(__name__)


@app.command()
def chat():
    console.print("[bold green]AI Agent CLI Chat[/bold green]")
    while True:
        try:
            message = input("You: ")
            if message.lower() in {"exit", "quit"}:
                break
            # пока просто echo
            log.info("user_message", message=message)
            console.print(f"[cyan]Agent:[/cyan] {message}")
        except KeyboardInterrupt:
            break


@app.command()
def weather(city: str):
    """Check weather for a city"""
    tool = WeatherTool()
    result = asyncio.run(tool.run(WeatherInput(city=city)))
    console.print(f"[cyan]Agent:[/cyan] {result}")


if __name__ == "__main__":
    app()
