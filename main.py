from fastapi import FastAPI, HTTPException, Query
import httpx
from pydantic import BaseModel, ValidationError

class CurrentWeather(BaseModel):
    temperature_2m: float
    relative_humidity_2m: int


class WeatherUnits(BaseModel):
    temperature_2m: str
    relative_humidity_2m: str


class WeatherResponse(BaseModel):
    latitude: float
    longitude: float
    current: CurrentWeather
    current_units: WeatherUnits

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/weather", response_model=WeatherResponse)
def get_weather(
    latitude: float = Query(ge=-90, le=90),
    longitude: float = Query(ge=-180, le=180),
):
    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m",
    }

    try:
        response = httpx.get(url, params=params, timeout=10.0)
        response.raise_for_status()

    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504,
            detail="Weather provider timed out",
        )

    except httpx.HTTPError:
        raise HTTPException(
            status_code=502,
            detail="Could not retrieve weather data",
        )

    try:
        data = response.json()
    except ValueError:
        raise HTTPException(
            status_code=502,
            detail="Weather provider returned invalid JSON",
        )

    try:
        weather = WeatherResponse.model_validate(data)
    except ValidationError:
        raise HTTPException(
            status_code=502,
            detail="Weather provider returned an invalid response",
        )

    return weather
