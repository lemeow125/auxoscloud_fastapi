import logging

from tenacity import retry, stop_after_attempt, wait_fixed

from . import Repo

logger = logging.getLogger(__name__)


class Inverter(Repo):
    """Inverter Actions"""

    @retry(stop=stop_after_attempt(10), wait=wait_fixed(1), reraise=True)
    def get_inverter(self):
        url = f"{self.CONFIG.AUXSOL_BASE_URL}/archive/inverter/getPlantByInverterSN/{self.CONFIG.AUXSOL_INVERTER_SN}"
        try:
            response = self.CONFIG.SESSION.get(url, timeout=3)
            self._validate(response)
            return response.json().get("data")
        except Exception as e:
            logger.error(e)
            raise

    @retry(stop=stop_after_attempt(10), wait=wait_fixed(1), reraise=True)
    def get_inverter_details(self):
        url = f"{self.CONFIG.AUXSOL_BASE_URL}/archive/plant/findPlantDetail/{self.CONFIG.AUXSOL_INVERTER_SN}"
        try:
            response = self.CONFIG.SESSION.get(url, timeout=3)
            self._validate(response)
            return response.json().get("data")
        except Exception as e:
            logger.error(e)
            raise
