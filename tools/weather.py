from pydantic import BaseModel, Field
from core.config import settings
import httpx


class WeatherInput(BaseModel):
    city: str = Field(..., description='City name to fetch weather for')


class WeatherTool:
    name = 'weather'
    description = "Fetch current weather for a city"

    async def run(self, payload: WeatherInput):
        if not settings.weather_api_key:
            return 'Weather API key not set.'

        url = "https://api.openweathermap.org/data/2.5/weather"
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                url, params={"q": payload.city, "appid": settings.weather_api_key, "units": "metric"}
            )
            if resp.status_code != 200:
                return f"Error: {resp.text}"
            data = resp.json()
            temp = data["main"]["temp"]
            desc = data["weather"][0]["description"]
            return f"In {payload.city}, it is {temp}°C with {desc}."
