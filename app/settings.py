from pydantic_settings import BaseSettings


class SchedulerSettings(BaseSettings):
    CALLBACK_SCHEDULE_ARN: str = ""
    ROLE_ARN: str = ""


class AwsSettings(SchedulerSettings):
    AWS_REGION: str = "eu-north-1"


class Settings(AwsSettings):
    APP_ID: str = ""
    SERVER_ID: str = ""
    BOT_TOKEN: str = ""
    CLIENT_PUBLIC_KEY: str = ""
    COMMANDS_FILENAME: str = "commands.json"
    DEBUG: bool = False

    class Config:
        env_file = ".env"


settings = Settings()
