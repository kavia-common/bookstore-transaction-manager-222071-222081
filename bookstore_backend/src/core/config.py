import os
from functools import lru_cache
from typing import List

from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings loaded from environment variables.

    Use this to access configuration like SECRET_KEY, DB URL, and CORS origin list.
    """

    def __init__(self) -> None:
        # Security and JWT
        self.SECRET_KEY: str = os.getenv("SECRET_KEY", "CHANGE_ME_DEV_SECRET")
        self.ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
        self.ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")

        # Database
        self.DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./bookstore.db")

        # CORS
        allow_origins_env = os.getenv("ALLOW_ORIGINS", "*")
        if allow_origins_env.strip() == "*":
            self.ALLOW_ORIGINS: List[str] = ["*"]
        else:
            self.ALLOW_ORIGINS = [o.strip() for o in allow_origins_env.split(",") if o.strip()]


# PUBLIC_INTERFACE
@lru_cache()
def get_settings() -> Settings:
    """Get cached application settings loaded from environment."""
    return Settings()
