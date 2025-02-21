from typing import Generator, Any
from unittest.mock import Mock, patch

import pytest
from fastapi.testclient import TestClient

from app.app_setup import default_app_factory
from app.settings import Settings, get_settings


@pytest.fixture(autouse=True)
def ollama_client_mock() -> Generator[Mock, None, None]:
    with patch("app.service.Client") as ollama_client_mock:
        ollama_client_mock.return_value = ollama_client_mock

        yield ollama_client_mock


@pytest.fixture
def api_test_client(socket_enabled: Any, default_settings: Settings) -> Generator[TestClient, None, None]:
    _ = socket_enabled

    app = default_app_factory()

    app.dependency_overrides[get_settings] = lambda: default_settings

    with TestClient(app, raise_server_exceptions=False) as api_test_client:
        yield api_test_client
