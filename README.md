# GreenAPI

A beginner-friendly climate and weather API built with Python and FastAPI. GreenAPI retrieves current weather information from the [Open-Meteo API](https://open-meteo.com/).

## Features

- Health-check endpoint
- Weather lookup using latitude and longitude
- Current temperature and relative humidity
- Input validation through FastAPI
- Interactive API documentation

## Tech Stack

- Python
- FastAPI
- HTTPX
- Open-Meteo API
- uv for dependency management

## Getting Started

### Prerequisites

- Python 3.12
- uv

### Installation

Clone this repository and enter the project directory:

```bash
git clone https://github.com/PadmaI1/green-api.git
cd green-api
```

Install the project dependencies:

```bash
uv sync
```

### Run the API

```bash
uv run fastapi dev main.py
```

The local API server will be available at `http://127.0.0.1:8000`.

## API Endpoints

### 1. Health Check

**GET `/health`**

Checks whether the API is responding.

Example response:

```json
{
  "status": "ok"
}
```

### 2. Current Weather

**GET `/weather`**

Accepts two required query parameters:

| Parameter | Type | Description |
|---|---|---|
| `latitude` | Float | Latitude of the requested location |
| `longitude` | Float | Longitude of the requested location |

Example request:

```text
/weather?latitude=18.5204&longitude=73.8567
```

Example response structure:

```json
{
  "latitude": 18.52,
  "longitude": 73.86,
  "current": {
    "temperature_2m": 27.4,
    "relative_humidity_2m": 65
  },
  "current_units": {
    "temperature_2m": "°C",
    "relative_humidity_2m": "%"
  }
}
```

*The values above are illustrative; actual weather readings and returned fields may differ.*

## Error Handling

- `422 Unprocessable Entity`: a required parameter is missing or has an invalid type.
- `502 Bad Gateway`: the upstream weather request failed.
- `504 Gateway Timeout`: the upstream weather provider timed out.

## Interactive Documentation

With the server running, visit:

`http://127.0.0.1:8000/docs`

Use the interactive documentation to explore and execute requests.

## Learning Goals

This project practises HTTP APIs, query parameters, input validation, external API integration, error handling, and developer documentation.