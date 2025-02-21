from functools import lru_cache
from typing import Annotated

from fastapi.params import Depends
from pydantic import AnyUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="everything_api_", frozen=True)

    ollama_host: AnyUrl
    ollama_port: int
    ollama_model: str = "llama3.2"

    @property
    def ollama_full_url(self) -> str:
        host = str(self.ollama_host)
        if host.endswith("/"):
            host = host[:-1]

        return f"{host}:{self.ollama_port}"


@lru_cache
def get_settings() -> Settings:  # pragma: no cover
    return Settings()


SettingsDep = Annotated[Settings, Depends(get_settings)]
