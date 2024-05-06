from datetime import datetime, timedelta
from uuid import UUID

import pytest

from app.exceptions import InvalidOptionsCount
from app.schemas import DiscordRequestData, Command, Option, OptionName, DATE_SEPARATOR, TIME_SEPARATOR
from app.settings import settings
from app.utils.operation import plan_meeting


@pytest.fixture
def discord_request_data():
    return DiscordRequestData(options=[
        Option(name=OptionName.DATE, value="25/02"),
        Option(name=OptionName.TIME, value="15:00"),
        Option(name=OptionName.DESCRIPTION, value="mock-description")
    ], name=Command.PLAN)


@pytest.fixture
def mock_logging(mocker):
    return mocker.patch("app.utils.operation.logger")


async def schedule(*args, **kwargs):
    pass


def uuid4() -> UUID:
    return UUID("00000000-0000-0000-0000-000000000000")


def parse_fields(length, separator, value, convert):
    return [25, 2] if separator == DATE_SEPARATOR else [15, 0]


@pytest.mark.asyncio
async def test_plan_meeting_should_raise_exception_when_invalid_options_count():
    false_discord_request_data = DiscordRequestData(options=[], name=Command.PLAN)

    with pytest.raises(InvalidOptionsCount):
        await plan_meeting(false_discord_request_data)


@pytest.mark.asyncio
async def test_plan_meeting_should_return_message_content_when_valid_options_count(
        mock_logging,
        mocker,
        discord_request_data
):
    mocked_uuid4 = mocker.patch("app.utils.operation.uuid4", return_value=uuid4())
    mocked_parse_field = mocker.patch("app.utils.operation.parse_fields", side_effect=parse_fields)
    mocked_schedule = mocker.patch("app.utils.operation.schedule", side_effect=schedule)

    date = discord_request_data.options[0].value
    time = discord_request_data.options[1].value
    description = discord_request_data.options[2].value
    message_content = await plan_meeting(discord_request_data)

    assert message_content == f"Meeting meeting-{uuid4()} planned for {date} at {time} - {description}"
    mocked_uuid4.assert_called_once()
    mocked_parse_field.assert_any_call(2, DATE_SEPARATOR, date, int)
    mocked_parse_field.assert_any_call(2, TIME_SEPARATOR, time, int)

    current_date = datetime(datetime.now().year, 2, 25, 15, 0)
    current_date -= timedelta(minutes=settings.MINUTES_REMINDER)

    mocked_schedule.assert_called_once_with(
        name=f"meeting-{uuid4()}",
        description=description,
        year=current_date.year,
        month=current_date.month,
        day=current_date.day,
        hour=current_date.hour,
        minute=current_date.minute
    )
    mock_logging.info.assert_called_once()
