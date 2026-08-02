import logging

from tenacity import retry, stop_after_attempt, wait_fixed

from . import Repo

logger = logging.getLogger(__name__)


class Analytics(Repo):
    """Analytics Actions"""

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(1), reraise=True)
    def get_analytics(self):
        url = f"{self.CONFIG.AUXSOL_BASE_URL}/analysis/plantReport/queryPlantCurrentDataAll?plantId={self.CONFIG.AUXSOL_INVERTER_ID}"
        try:
            response = self.CONFIG.SESSION.get(url, timeout=3)
            self._validate(response)
            return response.json().get("data")
        except Exception as e:
            logger.error(e)
            raise

    @retry(stop=stop_after_attempt(10), wait=wait_fixed(1), reraise=True)
    def get_inverter_report(self):
        url = f"{self.CONFIG.AUXSOL_BASE_URL}/analysis/inverterReport/findInverterRealTimeInfoBySnV1?sn={self.CONFIG.AUXSOL_INVERTER_SN}"
        try:
            response = self.CONFIG.SESSION.get(url, timeout=3)
            self._validate(response)
            return response.json().get("data")
        except Exception as e:
            logger.error(e)
            raise
