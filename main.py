from fastapi import FastAPI, HTTPException
from api.auxos import AuxsolClient

app = FastAPI()


@app.get("/")
async def status():
    """Healthcheck endpoint"""
    return {"status": "healthy"}


@app.get("/api/analytics/")
async def get_analytics():
    """
    Endpoint to get latest analytics data for inverter
    """
    try:
        with AuxsolClient() as client:
            res = client.analytics.get_analytics()
            if res and res.get("code") == "AWX-0000":
                data = res.get("data", {})
                energy = data.get("energyData", {})

                return {"data": energy}
            raise Exception(f"Request Failed: {res}")
    except Exception as e:
        raise HTTPException({"error": str(e)}, status_code=500)


@app.get("/api/analytics/inverter")
async def get_inverter_report():
    """
    Endpoint to get latest analytics report on inverter
    """
    try:
        with AuxsolClient() as client:
            res = client.analytics.get_inverter_report()
            if res and res.get("code") == "AWX-0000":
                data = res.get("data", {})

                return {"data": data}
            raise Exception(f"Request Failed: {res}")
    except Exception as e:
        raise HTTPException({"error": str(e)}, status_code=500)


@app.get("/api/inverter")
def get_inverter():
    """
    Endpoint to get latest info on inverter
    """
    try:
        with AuxsolClient() as client:
            res = client.inverters.get_inverter()
            if res and res.get("code") == "AWX-0000":
                data = res.get("data", {})

                return {"data": data}
            raise Exception(f"Request Failed: {res}")
    except Exception as e:
        raise HTTPException({"error": str(e)}, status_code=500)
