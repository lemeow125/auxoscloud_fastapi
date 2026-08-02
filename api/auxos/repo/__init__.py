__all__ = ["Auth", "Analytics", "Inverter"]


class Repo:
    """Base repo"""

    def __init__(self, CONFIG):
        self.CONFIG = CONFIG

    def _validate(self, res):
        """Validate response code success"""
        if not res:
            raise Exception(f"Request Failed: {str(res)}")
        try:
            if res.json().get("code") != "AWX-0000":
                raise Exception(f"Request Failed: {str(res)}")
        except Exception:
            raise Exception(f"Request Failed: {str(res)}")
