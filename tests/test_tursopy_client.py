import os

import pytest
import responses

from tests.conftest import TURSO_TOKEN_VALIDATION_URL
from tursopy import TursoClient
from tursopy.dataclasses import PlatformTokenRead
from tursopy.exceptions import InvalidPlatformTokenException, TursoRequestException


class TestTursoClient:
    @responses.activate
    def test_load_config_from_kwargs(self, dummy_settings: dict[str, str]) -> None:
        responses.add(responses.GET, TURSO_TOKEN_VALIDATION_URL, json={}, status=200)
        client = TursoClient(**dummy_settings)
        assert isinstance(client, TursoClient)

    @responses.activate
    def test_load_config_from_env(self) -> None:
        os.environ["turso_platform_token"] = "some-token"
        responses.add(responses.GET, TURSO_TOKEN_VALIDATION_URL, json={}, status=200)
        client = TursoClient()
        assert isinstance(client, TursoClient)

    def test_load_config_fails(self) -> None:
        with pytest.raises(Exception):
            TursoClient()

    @responses.activate
    def test_invalid_token_raises_error(self, client: TursoClient) -> None:
        os.environ["turso_platform_token"] = "some-token"
        responses.add(
            responses.GET, "https://api.turso.tech/v1/auth/validate", json={"error": "some error"}, status=401
        )
        with pytest.raises(InvalidPlatformTokenException):
            TursoClient()

    @responses.activate
    def test_list_platform_tokens_successful(self, client: TursoClient) -> None:
        responses.add(
            responses.GET,
            "https://api.turso.tech/v1/auth/api-tokens",
            json={"tokens": [{"id": "clGFZ4STEe6fljpFzIum8A", "name": "my-token"}]},
            status=200,
        )
        tokens = client.list_platform_tokens()
        assert isinstance(tokens, list)
        assert all([isinstance(x, PlatformTokenRead) for x in tokens])
        assert tokens[0].name == "my-token"
        assert tokens[0].id == "clGFZ4STEe6fljpFzIum8A"

    @responses.activate
    def test_list_platform_tokens_fails(self, client: TursoClient) -> None:
        responses.add(
            responses.GET, "https://api.turso.tech/v1/auth/api-tokens", json={"error": "some error"}, status=401
        )
        with pytest.raises(TursoRequestException):
            client.list_platform_tokens()
