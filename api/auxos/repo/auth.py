import logging
from . import Repo
from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)


class Auth(Repo):
    """Auth Actions"""

    @retry(stop=stop_after_attempt(10), wait=wait_exponential(multiplier=2, max=15))
    def login(self):
        try:
            url = f"{self.CONFIG.AUXSOL_BASE_URL}/auth/login"

            response = self.CONFIG.SESSION.post(
                url,
                json={
                    "account": self.CONFIG.AUXSOL_AUTH_USER,
                    "password": self.CONFIG.AUXSOL_AUTH_PASSWORD,
                    "lang": "en-US",
                },
                timeout=10,
            )

            self._validate(response)
            response = response.json()
            token = response.get("data").get("access_token")
            if token:
                self.CONFIG.SESSION.headers.update(
                    {
                        "Authorization": f"Bearer {token}",
                        "token": token,
                        "language": "2",
                    }
                )
            else:
                raise Exception(f"Login Failed: {response.json}")
        except Exception as e:
            logger.error(e)
            raise
