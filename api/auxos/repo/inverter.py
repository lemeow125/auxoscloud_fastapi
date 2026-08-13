import logging
import uuid
from datetime import datetime, timedelta, timezone

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

    @retry(stop=stop_after_attempt(10), wait=wait_fixed(1), reraise=True)
    def get_parameter_metadata(
        self, parameter_name: str, parent_id: str = "400", param_type: str = "readset"
    ):
        """
        Fetch parameter metadata (definition + optional current value).

        :param parameter_name: Display name of the parameter (e.g., "Battery Reserve SOC")
        :param parent_id: Parameter group ID (default "400")
        :param param_type: "readset" for definition template, "read" for live values
        :return: The parameter dictionary as returned by the API
        """
        sn = self.CONFIG.AUXSOL_INVERTER_SN
        url = f"{self.CONFIG.AUXSOL_BASE_URL}/analysis/inverterParam/queryParameterDataMeun"
        params = {
            "parameterParentId": parent_id,
            "paramType": param_type,
            "sn": sn,
        }
        response = self.CONFIG.SESSION.get(url, params=params, timeout=10)
        self._validate(response)
        data = response.json().get("data", {})
        for param in data.get(parent_id, []):
            if param.get("dataItemName") == parameter_name:
                return param
        raise ValueError(f"Parameter '{parameter_name}' not found for inverter {sn}")

    @retry(stop=stop_after_attempt(10), wait=wait_fixed(1), reraise=True)
    def set_battery_reserve_soc(self, value: int):
        """Set Battery Reserve SOC using live metadata."""
        # Fetch the definition template (without a live value)
        param_def = self.get_parameter_metadata(
            "Battery Reserve SOC", param_type="readset"
        )

        param = param_def.copy()
        param["dataItemValue"] = str(value)
        param["paramLastTime"] = datetime.now(timezone(timedelta(hours=8))).strftime(
            "%Y-%m-%d %H:%M:%S (+08:00)"
        )

        payload = {
            "sn": self.CONFIG.AUXSOL_INVERTER_SN,
            "batchNo": uuid.uuid4().hex,
            "sendType": "set",
            "parameterDataNew": [param],
        }

        url = f"{self.CONFIG.AUXSOL_BASE_URL}/analysis/inverterParam/parameterSendV1"
        response = self.CONFIG.SESSION.put(url, json=payload, timeout=10)
        self._validate(response)
        return response.json()
