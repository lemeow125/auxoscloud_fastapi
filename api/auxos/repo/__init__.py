import logging
from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)


class Auth:
    """Auth Actions"""

    def __init__(self, **kwargs):
        self.session = kwargs.get("session")
        self.BASE_URL = kwargs.get("base_url")
        self.USERNAME = kwargs.get("username")
        self.PASSWORD = kwargs.get("password")

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=2, max=15))
    def login(self):
        try:
            url = f"{self.BASE_URL}/auth/login"

            res = self.session.post(
                url,
                json={
                    "account": self.USERNAME,
                    "password": self.PASSWORD,
                    "lang": "en-US",
                },
                timeout=10
            )

            res = res.json()
            if res.get("code") == "AWX-0000":
                token = res.get("data", {}).get("access_token")
                if token:
                    self.session.headers.update(
                        {
                            "Authorization": f"Bearer {token}",
                            "token": token,
                            "language": "2",
                        }
                    )
                else:
                    raise Exception("Login Failed")
        except Exception as e:
            logger.error(e)
            raise


class Analytics:
    """Analytics Actions"""

    def __init__(self, **kwargs):
        self.session = kwargs.get("session")
        self.BASE_URL = kwargs.get("base_url")
        self.INVERTER_ID = kwargs.get("inverter_id")
        self.INVERTER_SN = kwargs.get("inverter_sn")

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=2, max=15))
    def get_analytics(self):
        url = f"{self.BASE_URL}/analysis/plantReport/queryPlantCurrentDataAll?plantId={self.INVERTER_ID}"
        try:
            response = self.session.get(url, timeout=15)
            return response.json()
        except Exception as e:
            logger.error(e)
            raise

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=2, max=15))
    def get_inverter_report(self):
        url = f"{self.BASE_URL}/analysis/inverterReport/findInverterRealTimeInfoBySnV1?sn={self.INVERTER_SN}"
        try:
            response = self.session.get(url, timeout=15)
            return response.json()
        except Exception as e:
            logger.error(e)
            raise


class Inverter:
    """Inverter Actions"""

    def __init__(self, **kwargs):
        self.session = kwargs.get("session")
        self.BASE_URL = kwargs.get("base_url")
        self.INVERTER_ID = kwargs.get("inverter_id")
        self.INVERTER_SN = kwargs.get("inverter_sn")

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=2, max=15))
    def get_inverter(self):
        url = f"{self.BASE_URL}/archive/inverter/getPlantByInverterSN/{self.INVERTER_SN}"
        try:
            response = self.session.get(url, timeout=15)
            return response.json()
        except Exception as e:
            logger.error(e)
            raise
