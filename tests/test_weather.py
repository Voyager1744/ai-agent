import pytest
import asyncio
from tools.weather import WeatherTool, WeatherInput


@pytest.mark.asyncio
async def test_weather_invalid_key(monkeypatch):
    monkeypatch.setenv("WEATHER_API_KEY", "")
    tool = WeatherTool()
    result = await tool.run(WeatherInput(city="London"))
    assert "London" in result
