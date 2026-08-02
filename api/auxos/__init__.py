from api.auxos.repo.analytics import Analytics
from api.auxos.repo.auth import Auth
from api.auxos.repo.battery import Battery
from api.auxos.repo.inverter import Inverter
from config import Config

class AuxsolClient:
    def __init__(self):
        self.CONFIG = Config().get_config()
        self.auth = None
        self.analytics = None
        self.inverters = None
        self.batteries = None

    def __enter__(self):
        """Create connection and session"""
        self.auth = Auth(self.CONFIG)
        self.auth.login()
        self.analytics = Analytics(self.CONFIG)
        self.inverters = Inverter(self.CONFIG)
        self.batteries = Battery(self.CONFIG)
        return self

    def __exit__(self, exc_type, exc_aval, exc_tb):
        """Close session"""
        self.CONFIG.SESSION.close()
