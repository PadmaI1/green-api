import httpx
import main
from fastapi.testclient import TestClient


client = TestClient(main.app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_weather_valid_coordinates(monkeypatch):
    def fake_get(url, params, timeout):
        return httpx.Response(
            200,
            json={
                "latitude": 18.5,
                "longitude": 73.8,
                "current": {
                    "temperature_2m": 29.4,
                    "relative_humidity_2m": 61,
                },
                "current_units": {
                    "temperature_2m": "°C",
                    "relative_humidity_2m": "%",
                },
            },
            request=httpx.Request("GET", url),
        )

    monkeypatch.setattr(main.httpx, "get", fake_get)

    response = client.get(
        "/weather",
        params={"latitude": 18.5, "longitude": 73.8},
    )

    assert response.status_code == 200

    data = response.json()
    assert data["latitude"] == 18.5
    assert data["current"]["temperature_2m"] == 29.4
    assert data["current"]["relative_humidity_2m"] == 61
    assert data["current_units"]["temperature_2m"] == "°C"


def test_weather_rejects_invalid_latitude():
    response = client.get(
        "/weather",
        params={"latitude": 150, "longitude": 73.8},
    )

    assert response.status_code == 422


def test_weather_rejects_invalid_longitude():
    response = client.get(
        "/weather",
        params={"latitude": 18.5, "longitude": 181},
    )

    assert response.status_code == 422


def test_weather_provider_timeout(monkeypatch):
    def fake_get(url, params, timeout):
        raise httpx.TimeoutException("simulated timeout")

    monkeypatch.setattr(main.httpx, "get", fake_get)

    response = client.get(
        "/weather",
        params={"latitude": 18.5, "longitude": 73.8},
    )

    assert response.status_code == 504
    assert response.json()["detail"] == "Weather provider timed out"


def test_weather_provider_http_error(monkeypatch):
    def fake_get(url, params, timeout):
        return httpx.Response(
            503,
            request=httpx.Request("GET", url),
        )

    monkeypatch.setattr(main.httpx, "get", fake_get)

    response = client.get(
        "/weather",
        params={"latitude": 18.5, "longitude": 73.8},
    )

    assert response.status_code == 502


def test_weather_provider_invalid_json(monkeypatch):
    def fake_get(url, params, timeout):
        return httpx.Response(
            200,
            text="this is not JSON",
            request=httpx.Request("GET", url),
        )

    monkeypatch.setattr(main.httpx, "get", fake_get)

    response = client.get(
        "/weather",
        params={"latitude": 18.5, "longitude": 73.8},
    )

    assert response.status_code == 502
    assert response.json()["detail"] == (
        "Weather provider returned invalid JSON"
    )


def test_weather_provider_invalid_data(monkeypatch):
    def fake_get(url, params, timeout):
        return httpx.Response(
            200,
            json={
                "latitude": 18.5,
                "longitude": 73.8,
                "current": {},
                "current_units": {},
            },
            request=httpx.Request("GET", url),
        )

    monkeypatch.setattr(main.httpx, "get", fake_get)

    response = client.get(
        "/weather",
        params={"latitude": 18.5, "longitude": 73.8},
    )

    assert response.status_code == 502
    assert response.json()["detail"] == (
        "Weather provider returned an invalid response"
    )