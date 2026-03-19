"""
Common model schemas
"""

from pydantic import (
    BaseModel,
    Field,
    StrictStr,
)


class Config(BaseModel):
    """
    Pydantic Configuration model for FastAPI
    """
    AUXSOL_BASE_URL: StrictStr = Field(
        default="https://eu.auxsolcloud.com/auxsol-api",
        json_schema_extra={"required": False},
        description="Auxsol base URL used for API calls"
    )
    AUXSOL_HOME_URL: StrictStr = Field(
        default="https://www.auxsolcloud.com",
        json_schema_extra={"required": False},
        description="Auxsol home URL used for API calls"
    )
    AUXSOL_AUTH_USER: StrictStr = Field(
        json_schema_extra={"required": True},
        description="Auxsol user email used for authenticating API calls"
    )
    AUXSOL_AUTH_PASSWORD: StrictStr = Field(
        json_schema_extra={"required": True},
        description="Auxsol user password used for authenticating API calls"
    )
    AUXSOL_INVERTER_ID: StrictStr = Field(
        json_schema_extra={"required": True},
        description="Auxsol inverter ID to poll for data via API"
    )
    AUXSOL_INVERTER_SN: StrictStr = Field(
        json_schema_extra={"required": True},
        description="Auxsol inverter serial number to poll for data via API"
    )
