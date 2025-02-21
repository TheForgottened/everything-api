import json
from typing import Any

from ollama import Client

from app.dto.http_response import HttpResponse
from app.mappers import map_query_params_list_to_dict
from app.settings import SettingsDep


class Service:
    def __init__(self, settings: SettingsDep) -> None:
        self._ollama_full_url = settings.ollama_full_url
        self._ollama_model = settings.ollama_model

        self._ollama_client = Client(host=self._ollama_full_url)

    def generate_response(
        self,
        method: str,
        path: str,
        headers: dict[str, str],
        query_params: list[tuple[str, str]],
        body: Any,
    ) -> HttpResponse:
        query_params_dict = map_query_params_list_to_dict(query_params=query_params)
        prompt = self._get_prompt(
            method=method, path=path, headers=headers, query_params_dict=query_params_dict, body=body
        )
        llm_response = self._ollama_client.generate(model=self._ollama_model, prompt=prompt, format="json")

        return HttpResponse.model_validate_json(json_data=llm_response["response"])

    @classmethod
    def _get_prompt(
        cls,
        method: str,
        path: str,
        headers: dict[str, str],
        query_params_dict: dict[str, list[str]],
        body: Any,
    ) -> str:
        request_data = {
            "httpMethod": method,
            "path": path,
            "headers": headers,
            "queryParams": query_params_dict,
            "body": body,
        }

        return (
            f"You are now a REST API. Look at the following JSON that contains all the information about the API "
            f"request and create a valid JSON response. Consider only what's inside the code block. Please answer with "
            f"only the JSON response and nothing else.\n\n"
            f"The JSON with the request information contains 5 keys:\n"
            f"- httpMethod: contains the HTTP method used on the request\n"
            f"- path: has the URI used on the request\n"
            f"- headers: contains another JSON object where the keys are the header name, and the values are the header "
            f"value\n"
            f"- queryParams: contains another JSON object where the keys are the query parameter name, and the "
            f"values are a list of all the values the query parameter was passed with\n"
            f"- body: the body of the HTTP request, can be anything\n\n"
            f"The JSON with the response information (the one you are generating) must contain only 3 keys:\n"
            f"- statusCode: the type must be integer, contains the HTTP status code of the response, may be any valid "
            f"HTTP status code you wish\n"
            f"- headers: the type must be a valid JSON object, contains all the headers you wish to return where the "
            f"key is the header name and the value is the header value\n"
            f"- body: the type must be a valid JSON object, that contains the body of the response, don't be afraid "
            f"to make it big\n\n"
            f"```json\n"
            f"{json.dumps(obj=request_data, indent=4, default=str)}"
            f"```\n"
        )
