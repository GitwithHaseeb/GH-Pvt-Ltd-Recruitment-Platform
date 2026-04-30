from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "GH Pvt Ltd Recruitment Platform"
    api_prefix: str = "/api"
    debug: bool = False

    database_url: str = "postgresql://postgres:postgres@db:5432/gh_recruitment"
    redis_url: str = "redis://redis:6379/0"

    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_pass: str = ""
    smtp_from: str = "GH Pvt Ltd <no-reply@ghpvtd.com>"

    admin_username: str = "admin"
    admin_password: str = "admin123"

    uploads_dir: str = "uploads"
    offer_letters_dir: str = "uploads/offer_letters"

    gmail_account_1: str = "ghaniatanveer061@gmail.com"
    gmail_account_2: str = "haseebch8130@gmail.com"
    gmail_api_credentials_path: str = "credentials.json"
    gmail_api_token_path: str = "token.json"

    celery_broker_url: str = "redis://redis:6379/0"
    celery_result_backend: str = "redis://redis:6379/1"


settings = Settings()
