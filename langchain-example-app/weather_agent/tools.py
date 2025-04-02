from typing import Optional, Type
from langchain.tools import BaseTool
from langchain.pydantic_v1 import BaseModel, Field
import requests

class WeatherInput(BaseModel):
    location: str = Field(..., description="The city or location to get weather for")

class WeatherTool(BaseTool):
    name: str = "get_weather"
    description: str = "Get current weather for a location"
    args_schema: Type[BaseModel] = WeatherInput

    def _get_weather_condition(self, code: int) -> str:
        conditions = {
            0: 'Clear sky',
            1: 'Mainly clear',
            2: 'Partly cloudy',
            3: 'Overcast',
            45: 'Foggy',
            48: 'Depositing rime fog',
            51: 'Light drizzle',
            53: 'Moderate drizzle',
            55: 'Dense drizzle',
            56: 'Light freezing drizzle',
            57: 'Dense freezing drizzle',
            61: 'Slight rain',
            63: 'Moderate rain',
            65: 'Heavy rain',
            66: 'Light freezing rain',
            67: 'Heavy freezing rain',
            71: 'Slight snow fall',
            73: 'Moderate snow fall',
            75: 'Heavy snow fall',
            77: 'Snow grains',
            80: 'Slight rain showers',
            81: 'Moderate rain showers',
            82: 'Violent rain showers',
            85: 'Slight snow showers',
            86: 'Heavy snow showers',
            95: 'Thunderstorm',
            96: 'Thunderstorm with slight hail',
            99: 'Thunderstorm with heavy hail',
        }
        return conditions.get(code, 'Unknown')

    def _run(self, location: str) -> str:
        # Geocoding
        geocoding_url = f"https://geocoding-api.open-meteo.com/v1/search?name={location}&count=1"
        geocoding_response = requests.get(geocoding_url)
        geocoding_data = geocoding_response.json()

        if not geocoding_data.get("results"):
            return f"Location '{location}' not found"

        location_data = geocoding_data["results"][0]
        latitude = location_data["latitude"]
        longitude = location_data["longitude"]
        location_name = location_data["name"]

        # Weather data
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,apparent_temperature,relative_humidity_2m,wind_speed_10m,wind_gusts_10m,weather_code"
        weather_response = requests.get(weather_url)
        weather_data = weather_response.json()

        current = weather_data["current"]
        condition = self._get_weather_condition(current["weather_code"])

        return (
            f"Weather in {location_name}:\n"
            f"Temperature: {current['temperature_2m']}°C\n"
            f"Feels like: {current['apparent_temperature']}°C\n"
            f"Humidity: {current['relative_humidity_2m']}%\n"
            f"Wind speed: {current['wind_speed_10m']} km/h\n"
            f"Wind gusts: {current['wind_gusts_10m']} km/h\n"
            f"Conditions: {condition}"
        )

    async def _arun(self, location: str) -> str:
        # 同期版を使用
        return self._run(location)