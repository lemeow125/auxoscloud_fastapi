"""
Common service functions and classes imported elsewhere.

"""

import os
import sys
from typing import Optional

from dotenv import find_dotenv, load_dotenv
from faker import Faker
from pydantic.fields import FieldInfo

from .models import Config as ConfigModel

fake = Faker()


class Config:
    """
    Core application config.
    """

    def __init__(self, prefix: Optional[str] = "backend") -> None:
        """
        Initialize the Config class.

        Args:
            prefix (str, optional): Prefix for environment variables. Defaults to "backend".
        """
        load_dotenv(find_dotenv())

        self.prefix = prefix.upper()

        # Check if run by Pytest
        if "pytest" in sys.modules:
            # Generate test config
            for field_name, field_info in ConfigModel.model_fields.items():
                setattr(
                    self, field_name, self._generate_faker_data(field_name, field_info)
                )
        else:
            # Use real config
            for field in ConfigModel.model_fields.items():
                setattr(self, field[0], self.set_env_var(field))

    def set_env_var(self, field: tuple):
        """
        Retrieve and sets an environment variable.

        Args:
            field (tuple): A tuple containing the field name and its FieldInfo.

        Returns:
            str: The value of the environment variable.

        Raises:
            RuntimeError: If required is True and the variable is not set.
        """

        # Unpack field info
        field_key = f"{self.prefix}_{field[0]}".upper()
        field_info: FieldInfo = field[1]

        # Fetch value, return field default value if not found
        field_value = os.getenv(field_key, field_info.default)

        # Cast to boolean if the expected type is bool
        if field_info.annotation is bool and isinstance(field_value, str):
            field_value = field_value.lower() in ("true", "1", "yes")

        return field_value

    def _generate_faker_data(self, field_name: str, field_info) -> any:
        """
        Generate placeholder data using faker based on field name and type.

        Args:
            field_name (str): The name of the field.
            field_info: The pydantic field info object.

        Returns:
            any: Generated placeholder data.
        """
        field_type = field_info.annotation

        # Handle specific field names
        if field_name == "AUXSOL_BASE_URL":
            return "https://eu.auxsolcloud.com/auxsol-api"
        elif field_name == "AUXSOL_HOME_URL":
            return "https://www.auxsolcloud.com"
        elif field_name == "AUXSOL_AUTH_USER":
            return fake.email()
        elif field_name == "AUXSOL_AUTH_PASSWORD":
            return fake.password(length=16, special_chars=True)
        elif field_name == "AUXSOL_INVERTER_ID":
            return fake.random_number(digits=8)
        elif field_name == "AUXSOL_INVERTER_SN":
            return fake.serial_number()

        # Fallback based on type hints
        if field_type is str:
            return fake.word()
        elif field_type is int:
            return fake.random_int(min=1, max=65535)
        elif field_type is bool:
            return fake.boolean()
        elif field_type is list:
            return []

        return None

    def get_config(self) -> ConfigModel:
        """
        Get the config model.

        Returns:
            ConfigModel: The config model instance.
        """
        return ConfigModel(**self.__dict__)
