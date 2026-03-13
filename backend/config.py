"""
Application configuration loaded from environment variables.
Copy .env.example to .env and adjust values for your deployment.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False

    # CORS — in production, set this to your frontend domain
    allowed_origins: list[str] = ["http://localhost:5173", "http://localhost:3000"]

    # File uploads
    upload_dir: str = "/tmp/pdf_highlights_uploads"
    max_upload_bytes: int = 100 * 1024 * 1024   # 100 MB
    upload_ttl_seconds: int = 3600               # delete after 1 hour

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
