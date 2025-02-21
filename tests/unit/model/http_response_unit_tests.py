import pytest

from app.dto.http_response import HttpResponse
from app.types import JSONable
from tests.testdoubles.ollama_response_doubles import ollama_response_01, ollama_response_dict_01

pytestmark = pytest.mark.unit_test


@pytest.mark.parametrize(
    ("string_body", "expected_body"), [(ollama_response_01()["response"], ollama_response_dict_01())]
)
def test_string_body_gets_parsed_to_dict_correctly(string_body: str, expected_body: JSONable):
    # When
    result = HttpResponse(status_code=200, headers={}, body=string_body)

    # Then
    assert result.body == expected_body
