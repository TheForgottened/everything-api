import json

from app.types import JSONable


def ollama_response_dict_01() -> JSONable:
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        "body": {
            "id": 12345,
            "name": "John Doe",
            "email": "john.doe@example.com",
            "created_at": "2024-12-23T12:34:56Z",
            "roles": ["user", "admin"],
            "active": True,
        },
    }


def ollama_response_01() -> JSONable:
    return {"response": json.dumps(ollama_response_dict_01())}
