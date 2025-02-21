from typing import Generator

import pytest

from app.settings import Settings


@pytest.fixture
def default_settings() -> Generator[Settings, None, None]:
    yield Settings(
        ollama_host="http://127.0.0.1",
        ollama_port=4321,
        ollama_model="testing1.0.1",
    )
