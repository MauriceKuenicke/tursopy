import os
from typing import Any, Optional

import requests

from .dataclasses import PlatformTokenCreated, PlatformTokenRead
from .db import DatabasesClient
from .endpoints import API_PATH
from .exceptions import (
    InvalidPlatformTokenException,
    MissingRequiredAttributeException,
    TokenAlreadyExistsException,
    TokenNotFoundException,
    TursoRequestException,
)


class TursoClient:
    """
    TursoClient main class.
    """

    def __init__(self, **kwargs: Any) -> None:
        """
        Initialize a Turso client.

        :param: token: Turso access token.
        """
        required_attributes = ["platform_token"]
        for attribute in required_attributes:
            value = self._fetch_config(attribute, **kwargs)
            if self._fetch_config(attribute, **kwargs) is None:
                required_message = (
                    f"Required configuration setting <'{attribute}'> missing."
                    "\nThis setting can be provided as a keyword argument to "
                    "the 'TursoClient' class constructor, "
                    f"or as an environment variable named 'turso_{attribute}'."
                )
                raise MissingRequiredAttributeException(required_message)
            else:
                setattr(self, attribute, value)

        self.base_url = "https://api.turso.tech"
        self.base_header = {
            "Authorization": f"Bearer {getattr(self, 'platform_token')}",
            "Content-Type": "application/json",
        }
        self._validate_user_token()
        self.db = DatabasesClient(base_client=self)

    @staticmethod
    def _fetch_config(attribute: str, **kwargs: Any) -> Optional[str]:
        """
        Fetch config either from the keyword argument or the environment variables.
        :param attribute:
        :return: Config value if exists. Otherwise, None.
        """
        args_config: Optional[str] = kwargs.get(attribute, None)
        env_value = os.getenv(f"turso_{attribute}", None)
        if args_config is not None:
            return args_config
        else:
            return env_value

    def _validate_user_token(self) -> bool:
        """
        Validate the current platform api token.
        :return:
        """
        endpoint = API_PATH["validate_platform_token"]
        request_url = self.base_url + endpoint
        response = requests.get(request_url, headers=self.base_header)

        if response.status_code == 401:
            error_message = response.json()["error"]
            raise InvalidPlatformTokenException(error_message)
        elif response.status_code != 200:
            raise TursoRequestException(f"Something went wrong: {response.content!r}")

        return True

    def create_platform_api_token(self, name: str) -> PlatformTokenCreated:
        """
        Request a Bearer token for platform access.
        :return: Platform API token.
        """
        endpoint = API_PATH["create_platform_token"].format(name=name)
        request_url = self.base_url + endpoint

        response = requests.post(request_url, headers=self.base_header)

        if response.status_code == 409:
            raise TokenAlreadyExistsException(f"Token with name <{name}> already exists.")
        elif response.status_code != 200:
            raise TursoRequestException(f"Something went wrong: {response.content!r}")

        content = response.json()
        return PlatformTokenCreated.load(content)

    def list_platform_tokens(self) -> list[PlatformTokenRead]:
        """
        Returns a list of API tokens belonging to a user.
        :return:
        """
        endpoint = API_PATH["list_platform_tokens"]
        request_url = self.base_url + endpoint
        response = requests.get(request_url, headers=self.base_header)

        if response.status_code != 200:
            raise TursoRequestException(f"Something went wrong: {response.content!r}")

        content = response.json()
        return [PlatformTokenRead.load(token) for token in content["tokens"]]

    def revoke_token(self, name: str) -> str:
        """
        Revokes the provided API token belonging to a user.
        :param name: Name of the api token.
        :return:
        """
        endpoint = API_PATH["revoke_platform_token"].format(name=name)
        request_url = self.base_url + endpoint
        response = requests.delete(request_url, headers=self.base_header)

        if response.status_code == 404:
            raise TokenNotFoundException(f"Token with name <{name}> not found.")
        if response.status_code != 200:
            raise TursoRequestException(f"Something went wrong: {response.content!r}")

        content: str = response.json()["token"]
        return content
