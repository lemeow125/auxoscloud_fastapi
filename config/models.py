"""
Common model schemas
"""

from requests import Session
from pydantic import BaseModel, Field, StrictStr, model_validator


class Config(BaseModel):
    """
    Pydantic Configuration model for FastAPI
    """
    model_config = {"arbitrary_types_allowed": True}

    AUXSOL_BASE_URL: StrictStr = Field(
        default="https://eu.auxsolcloud.com/auxsol-api",
        json_schema_extra={"required": False},
        description="Auxsol base URL used for API calls",
    )
    AUXSOL_HOME_URL: StrictStr = Field(
        default="https://www.auxsolcloud.com",
        json_schema_extra={"required": False},
        description="Auxsol home URL used for API calls",
    )
    AUXSOL_AUTH_USER: StrictStr = Field(
        json_schema_extra={"required": True},
        description="Auxsol user email used for authenticating API calls",
    )
    AUXSOL_AUTH_PASSWORD: StrictStr = Field(
        json_schema_extra={"required": True},
        description="Auxsol user password used for authenticating API calls",
    )
    AUXSOL_INVERTER_ID: StrictStr = Field(
        json_schema_extra={"required": True},
        description="Auxsol inverter ID to poll for data via API",
    )
    AUXSOL_INVERTER_SN: StrictStr = Field(
        json_schema_extra={"required": True},
        description="Auxsol inverter serial number to poll for data via API",
    )
    SESSION: Session = Field(
        json_schema_extra={"required": False},
        default_factory=Session,
        description="Session to use for API calls, constructed dynamically",
    )

    @model_validator(mode="after")
    def set_session_headers(self) -> "Config":
        """Set headers on the Session using the model's own fields."""
        session = self.SESSION
        session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:147.0) Gecko/20100101 Firefox/147.0",
                "Accept": "application/json, text/plain, */*",
                "Accept-Language": "en-US,en;q=0.5",
                "Content-Type": "application/json;charset=utf-8",
                "Origin": self.AUXSOL_HOME_URL,
                "Referer": self.AUXSOL_HOME_URL,
                "Connection": "keep-alive",
            }
        )
        return self
