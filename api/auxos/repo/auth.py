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
                timeout=10,
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
