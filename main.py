from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi_cache import FastAPICache
from fastapi_cache.backends.memcached import MemcachedBackend
from fastapi_cache.decorator import cache

from api.auxos import AuxsolClient


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    FastAPICache.init(MemcachedBackend, prefix="fastapi-cache")
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def status():
    """Healthcheck endpoint"""
    return {"status": "healthy"}


@cache(expire=5)
@app.get("/api/analytics/")
async def get_analytics():
    """
    Endpoint to get latest analytics data for inverter
    """
    try:
        with AuxsolClient() as client:
            data = client.analytics.get_analytics()
            return {"data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": str(e)})


@cache(expire=5)
@app.get("/api/analytics/inverter")
async def get_inverter_report():
    """
    Endpoint to get latest analytics report on inverter
    """
    try:
        with AuxsolClient() as client:
            data = client.analytics.get_inverter_report()
            return {"data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": str(e)})


@cache(expire=5)
@app.get("/api/inverter")
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


@cache(expire=5)
@app.get("/api/inverter/detail")
def get_inverter_details():
    """
    Endpoint to get latest details on inverter
    """
    try:
        with AuxsolClient() as client:
            data = client.inverters.get_inverter()
            return {"data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": str(e)})


@cache(expire=5)
@app.get("/api/battery")
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
