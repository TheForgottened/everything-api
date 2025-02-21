import json
from typing import Any

from pydantic import BaseModel, field_validator, ConfigDict
from pydantic.alias_generators import to_camel

from app.types import JSONable


class HttpResponse(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        validate_assignment=True,
        populate_by_name=True,
    )

    status_code: int
    headers: dict[str, str]
    body: JSONable

    @field_validator("headers", "body", mode="before")
    def _parse_str_to_dict(cls, value: Any) -> Any:
        if isinstance(value, str):
            return json.loads(value)

        return value
