import pytest

from app.exceptions import InvalidOptionsCount
from app.schemas import DiscordRequestData, Command, Option, OptionName
from app.utils.operation import cancel_meeting


@pytest.fixture
def discord_request_data():
    return DiscordRequestData(options=[
        Option(name=OptionName.NAME, value="mock-name")
    ], name=Command.CANCEL)


async def cancel_schedule(*args, **kwargs):
    pass


@pytest.fixture
def mock_logging(mocker):
    return mocker.patch("app.utils.operation.logger")


@pytest.mark.asyncio
async def test_cancel_meeting_should_raise_exception_when_invalid_options_count():
    false_discord_request_data = DiscordRequestData(options=[], name=Command.CANCEL)

    with pytest.raises(InvalidOptionsCount):
        await cancel_meeting(false_discord_request_data)


@pytest.mark.asyncio
async def test_cancel_meeting_should_return_message_content_when_valid_options_count(
        mock_logging,
        mocker,
        discord_request_data
):
    mocked_cancel_schedule = mocker.patch("app.utils.operation.cancel_schedule", side_effect=cancel_schedule)

    name = discord_request_data.options[0].value
    message_content = await cancel_meeting(discord_request_data)

    assert message_content == f"Meeting {name} cancelled"
    mocked_cancel_schedule.assert_called_once()
    mock_logging.info.assert_called_once()
