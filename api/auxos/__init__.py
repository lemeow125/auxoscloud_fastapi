import requests

from api.auxos.repo import Analytics, Auth, Inverter
from config import Config

config = Config().get_config()


class AuxsolClient:
    def __init__(self):
        self.BASE_URL = config.AUXSOL_BASE_URL
        self.HOME_URL = config.AUXSOL_HOME_URL
        self.USERNAME = config.AUXSOL_AUTH_USER
        self.PASSWORD = config.AUXSOL_AUTH_PASSWORD
        self.INVERTER_ID = config.AUXSOL_INVERTER_ID
        self.INVERTER_SN = config.AUXSOL_INVERTER_SN
        self.session = requests.Session()

        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:147.0) Gecko/20100101 Firefox/147.0",
                "Accept": "application/json, text/plain, */*",
                "Accept-Language": "en-US,en;q=0.5",
                "Content-Type": "application/json;charset=utf-8",
                "Origin": self.HOME_URL,
                "Referer": self.HOME_URL,
                "Connection": "keep-alive",
            }
        )

        self.auth = None
        self.analytics = None
        self.inverters = None

    def __enter__(self):
        """Create connection and session"""
        self.auth = Auth(
            session=self.session,
            base_url=self.BASE_URL,
            username=self.USERNAME,
            password=self.PASSWORD,
        )
        self.auth.login()
        self.analytics = Analytics(
            session=self.session,
            base_url=self.BASE_URL,
            inverter_id=self.INVERTER_ID,
            inverter_sn=self.INVERTER_SN,
        )

        self.inverters = Inverter(
            session=self.session,
            base_url=self.BASE_URL,
            inverter_id=self.INVERTER_ID,
            inverter_sn=self.INVERTER_SN,
        )
        return self

    def __exit__(self, exc_type, exc_aval, exc_tb):
        """Close session"""
        self.session.close()
