from typing import Generator
from unittest.mock import Mock, patch

import pytest

from app.service import Service
from app.settings import Settings
from tests.testdoubles.headers_dict_doubles import headers_dict_01
from tests.testdoubles.http_response_doubles import http_response_01
from tests.testdoubles.ollama_response_doubles import ollama_response_01
from tests.testdoubles.query_params_dict_doubles import query_params_dict_01
from tests.testdoubles.query_params_doubles import query_params_01
from tests.testutils.random_data_generator import (
    get_random_http_method,
    get_random_path,
    get_random_ascii_letters_string,
)

pytestmark = pytest.mark.unit_test


@pytest.fixture(autouse=True)
def ollama_client_mock() -> Generator[Mock, None, None]:
    with patch("app.service.Client") as ollama_client_mock:
        ollama_client_mock.return_value = ollama_client_mock

        yield ollama_client_mock


@pytest.fixture
def service(default_settings: Settings) -> Generator[Service, None, None]:
    yield Service(settings=default_settings)


def test_generate_response_correctly_calls_ollama(
    service: Service, default_settings: Settings, ollama_client_mock: Mock
):
    # Given
    default_method = get_random_http_method()
    default_path = get_random_path()
    default_headers = headers_dict_01()
    default_query_params = query_params_01()
    default_body = get_random_ascii_letters_string()

    expected_prompt = service._get_prompt(
        method=default_method,
        path=default_path,
        headers=default_headers,
        query_params_dict=query_params_dict_01(),
        body=default_body,
    )

    ollama_client_mock.generate.return_value = ollama_response_01()

    # When
    result = service.generate_response(
        method=default_method,
        path=default_path,
        headers=default_headers,
        query_params=default_query_params,
        body=default_body,
    )

    # Then
    ollama_client_mock.generate.assert_called_once()

    call_kwargs = ollama_client_mock.generate.call_args.kwargs
    assert call_kwargs["model"] == default_settings.ollama_model
    assert call_kwargs["prompt"] == expected_prompt
    assert call_kwargs["format"] == "json"

    assert result == http_response_01()
