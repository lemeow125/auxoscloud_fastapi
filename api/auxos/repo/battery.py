import logging

from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)


class Battery:
    """Battery Actions"""

    def __init__(self, **kwargs):
        self.SESSION = kwargs.get("session")
        self.BASE_URL = kwargs.get("base_url")
        self.INVERTER_ID = kwargs.get("inverter_id")
        self.INVERTER_SN = kwargs.get("inverter_sn")

    @retry(stop=stop_after_attempt(10), wait=wait_exponential(multiplier=2, max=15))
    def get_battery_details(self):
        url = f"{self.BASE_URL}/analysis/inverterReport/findInverterRealTimeInfoBySnV1?sn={self.INVERTER_SN}"
        try:
            response = self.SESSION.get(url, timeout=15)
            return response.json().get("batteryData")
        except Exception as e:
            logger.error(e)
            raise
