from typing import Any, Generator

import pytest
import responses

from tursopy import TursoClient

TURSO_TOKEN_VALIDATION_URL = "https://api.turso.tech/v1/auth/validate"


@pytest.fixture(autouse=True)
def block_all_non_mocked_requests() -> Generator[Any, Any, Any]:
    with responses.RequestsMock(assert_all_requests_are_fired=True):
        yield


@pytest.fixture
def dummy_settings() -> dict[str, str]:
    required_dummy_settings = {x: "dummy" for x in ["platform_token"]}
    return required_dummy_settings


@pytest.fixture
@responses.activate
def client(dummy_settings: dict[str, str]) -> TursoClient:
    responses.add(responses.GET, TURSO_TOKEN_VALIDATION_URL, json={}, status=200)
    client = TursoClient(**dummy_settings)
    return client
