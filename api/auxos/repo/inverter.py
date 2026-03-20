import logging

from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)


class Inverter:
    """Inverter Actions"""

    def __init__(self, **kwargs):
        self.session = kwargs.get("session")
        self.BASE_URL = kwargs.get("base_url")
        self.INVERTER_ID = kwargs.get("inverter_id")
        self.INVERTER_SN = kwargs.get("inverter_sn")

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=2, max=15))
    def get_inverter(self):
        url = (
            f"{self.BASE_URL}/archive/inverter/getPlantByInverterSN/{self.INVERTER_SN}"
        )
        try:
            response = self.session.get(url, timeout=15)
            return response.json()
        except Exception as e:
            logger.error(e)
            raise

    def get_inverter_details(self):
        url = f"{self.BASE_URL}/archive/plant/findPlantDetail/{self.INVERTER_SN}"
        try:
            response = self.session.get(url, timeout=15)
            return response.json()
        except Exception as e:
            logger.error(e)
            raise
