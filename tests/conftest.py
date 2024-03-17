from typing import Any, Generator

import pytest
import responses


@pytest.fixture(autouse=True)
def block_all_non_mocked_requests() -> Generator[Any, Any, Any]:
    with responses.RequestsMock(assert_all_requests_are_fired=True):
        yield
