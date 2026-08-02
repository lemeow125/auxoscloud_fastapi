import logging

from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)


class Inverter:
    """Inverter Actions"""

    def __init__(self, CONFIG):
        self.CONFIG = CONFIG

    @retry(stop=stop_after_attempt(10), wait=wait_exponential(multiplier=2, max=15))
    def get_inverter(self):
        url = (
            f"{self.CONFIG.AUXSOL_BASE_URL}/archive/inverter/getPlantByInverterSN/{self.CONFIG.AUXSOL_INVERTER_SN}"
        )
        try:
            response = self.CONFIG.SESSION.get(url, timeout=15)
            self._validate(response)
            return response.json().get("data")
        except Exception as e:
            logger.error(e)
            raise

    @retry(stop=stop_after_attempt(10), wait=wait_exponential(multiplier=2, max=15))
    def get_inverter_details(self):
        url = f"{self.CONFIG.AUXSOL_BASE_URL}/archive/plant/findPlantDetail/{self.CONFIG.AUXSOL_INVERTER_SN}"
        try:
            response = self.CONFIG.SESSION.get(url, timeout=15)
            self._validate(response)
            return response.json().get("data")
        except Exception as e:
            logger.error(e)
            raise
