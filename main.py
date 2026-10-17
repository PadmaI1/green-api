from fastapi import FastAPI
import httpx

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/weather")
def get_weather(latitude: float, longitude: float):
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

    data = response.json()

    return {
        "latitude": data["latitude"],
        "longitude": data["longitude"],
        "current": data["current"],
        "current_units": data["current_units"],
    }
