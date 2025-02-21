from unittest.mock import Mock

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.config.constants import HTTP_METHODS_LIST
from tests.testdoubles.headers_dict_doubles import headers_dict_01
from tests.testdoubles.ollama_response_doubles import ollama_response_01, ollama_response_dict_01
from tests.testdoubles.query_params_doubles import query_params_01
from tests.testutils.random_data_generator import get_random_path, get_random_ascii_letters_string

pytestmark = pytest.mark.integration_test


@pytest.mark.parametrize("http_method", HTTP_METHODS_LIST)
def test_do(http_method: str, api_test_client: TestClient, ollama_client_mock: Mock):
    # Given
    default_path = get_random_path()
    default_headers = headers_dict_01()
    default_query_params = query_params_01()
    default_body = get_random_ascii_letters_string()

    ollama_client_mock.generate.return_value = ollama_response_01()

    # When
    response = api_test_client.request(
        method=http_method,
        url=default_path,
        content=default_body,
        headers=default_headers,
        params=default_query_params,
    )

    # Then
    expected_response_dict = ollama_response_dict_01()

    assert response.status_code == expected_response_dict["statusCode"]
    if http_method.lower() != "head":
        assert response.json() == expected_response_dict["body"]

    for key, value in expected_response_dict["headers"].items():
        assert key in response.headers
        assert value == response.headers[key]


def test_exception_handler(api_test_client: TestClient, ollama_client_mock: Mock):
    # Given
    ollama_client_mock.generate.side_effect = RuntimeError("An unexpected error happened!")

    # When
    response = api_test_client.get("anything")

    # Then
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json() == {"description": "Unexpected internal server error."}