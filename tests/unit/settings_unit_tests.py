import pytest

from app.settings import Settings

pytestmark = pytest.mark.unit_test


@pytest.mark.parametrize(
    ("ollama_host", "ollama_port", "expected_result"),
    [
        ("http://127.0.0.1", "11434", "http://127.0.0.1:11434"),
        ("https://127.0.0.1", "11434", "https://127.0.0.1:11434"),
        ("https://llm.everything.com", "11434", "https://llm.everything.com:11434"),
        ("https://llm.everything.com/", "11434", "https://llm.everything.com:11434"),
    ],
)
def test_ollama_full_url(ollama_host: str, ollama_port: int, expected_result: str, default_settings: Settings):
    # Given
    default_settings.model_config["frozen"] = False

    default_settings.ollama_host = ollama_host
    default_settings.ollama_port = ollama_port

    # When
    result = default_settings.ollama_full_url

    # Then
    assert result == expected_result
