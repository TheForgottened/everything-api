from app.dto.http_response import HttpResponse
from tests.testdoubles.ollama_response_doubles import ollama_response_dict_01


def http_response_01() -> HttpResponse:
    return HttpResponse.model_validate(ollama_response_dict_01())
