__all__ = ["Auth", "Analytics", "Inverter"]


class Repo:
    """Base repo"""

    def __init__(self, CONFIG):
        self.CONFIG = CONFIG

    def _validate(self, res):
        """Raise with the upstream body unless the envelope says success."""
        if res.status_code >= 400 or res.json().get("code") != "AWX-0000":
            raise Exception(res.text)
