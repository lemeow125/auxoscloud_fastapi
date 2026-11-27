from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.decorator import cache

from api.auxos import AuxsolClient

cache_ttl = 30
@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache")
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def status():
    """Healthcheck endpoint"""
    return {"status": "healthy"}


@app.get("/api/analytics/")
@cache(expire=cache_ttl)
def get_analytics():
    """
    Endpoint to get latest analytics data for inverter
    """
    try:
        with AuxsolClient() as client:
            data = client.analytics.get_analytics()
            return {"data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": str(e)})


@app.get("/api/analytics/inverter")
@cache(expire=cache_ttl)
def get_inverter_report():
    """
    Endpoint to get latest analytics report on inverter
    """
    try:
        with AuxsolClient() as client:
            data = client.analytics.get_inverter_report()
            return {"data": data}
    except Exception as e: 
        raise HTTPException(status_code=500, detail={"error": str(e)})


@app.get("/api/inverter")
@cache(expire=cache_ttl)
def get_inverter():
    """
    Endpoint to get latest info on inverter
    """
    try:
        with AuxsolClient() as client:
            data = client.inverters.get_inverter()
            return {"data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": str(e)})


@app.get("/api/inverter/detail")
@cache(expire=cache_ttl)
def get_inverter_details():
    """
    Endpoint to get latest details on inverter
    """
    try:
        with AuxsolClient() as client:
            data = client.inverters.get_inverter_details()
            return {"data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": str(e)})


@app.get("/api/battery")
@cache(expire=cache_ttl)
def get_battery():
    """
    Endpoint to get latest info on batteries connected to inverter
    """
    try:
        with AuxsolClient() as client:
            data = client.batteries.get_battery_details()
            return {"data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": str(e)})


@app.post("/api/inverter/set-battery-reserve-soc")
def set_battery_reserve_soc(request: Request):
    try:
        body = request.json()
        value = body.get("value")
        if value is None:
            raise HTTPException(400, detail="Missing 'value' field")
        if not isinstance(value, int) or not (10 <= value <= 100):
            raise HTTPException(
                400, detail="Value must be an integer between 10 and 100"
            )

        with AuxsolClient() as client:
            result = client.inverters.set_battery_reserve_soc(value)
            return {"status": "success", "data": result}

    except ValueError as e:
        raise HTTPException(400, detail={"error": str(e)})
    except Exception as e:
        raise HTTPException(500, detail={"error": str(e)})
