import logging
from . import Repo
from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)


class Battery(Repo):
    """Battery Actions"""


    @retry(stop=stop_after_attempt(10), wait=wait_exponential(multiplier=2, max=15))
    def get_battery_details(self):
        url = f"{self.CONFIG.AUXSOL_BASE_URL}/analysis/inverterReport/findInverterRealTimeInfoBySnV1?sn={self.CONFIG.AUXSOL_INVERTER_SN}"
        try:
            response = self.CONFIG.SESSION.get(url, timeout=15)
            self._validate(response)
            return response.json().get("data").get("batteryData")
        except Exception as e:
            logger.error(e)
            raise
