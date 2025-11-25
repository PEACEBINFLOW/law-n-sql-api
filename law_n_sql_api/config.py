from __future__ import annotations
from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    Basic configuration for the API.

    You can extend this later with auth, CORS config, etc.
    """

    app_name: str = "Law-N SQL API"
    debug: bool = True

    class Config:
        env_prefix = "LAW_N_SQL_API_"


settings = Settings()
