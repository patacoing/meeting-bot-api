from pydantic import BaseModel, field_validator
from enum import Enum

DATE_SEPARATOR = "/"
TIME_SEPARATOR = ":"


class Command(Enum):
    PLAN = "plan"
    CANCEL = "cancel"


class OptionName(Enum):
    DATE = "date"
    TIME = "time"
    DESCRIPTION = "description"
    NAME = "name"


class EventBridgeAction(Enum):
    PING = "ping"


class EventBridgeRequest(BaseModel):
    action: EventBridgeAction
    name: str
    time: str
    description: str

    @classmethod
    @field_validator("time")
    def validate_time(cls, v):
        if len(v.split(TIME_SEPARATOR)) != 2:
            raise ValueError("Invalid time format")
        return v


class Option(BaseModel):
    name: OptionName
    type: int = 3
    value: str = ""

    @staticmethod
    @field_validator("value")
    def validate_value(cls, v):
        if cls.name == OptionName.DATE and len(v.split(DATE_SEPARATOR)) != 2:
            raise ValueError("Invalid date format")
        elif cls.name == OptionName.TIME and len(v.split(TIME_SEPARATOR)) != 2:
            raise ValueError("Invalid time format")
        return v


class DiscordType(Enum):
    PING = 1
    PONG = 1
    APP_COMMAND = 3
    RESPONSE = 4


class DiscordRequestData(BaseModel):
    name: Command
    options: list[Option]


class DiscordRequest(BaseModel):
    type: DiscordType
    data: DiscordRequestData | None = None


class DiscordResponseData(BaseModel):
    content: str


class DiscordResponse(BaseModel):
    type: DiscordType = DiscordType.RESPONSE
    data: DiscordResponseData | None = None
