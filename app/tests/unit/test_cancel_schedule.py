import pytest

from app.exceptions import ScheduleNotFound
from app.utils.schedule import cancel_schedule


@pytest.fixture
def mock_logging(mocker):
    return mocker.patch("app.utils.schedule.logger", autospec=True)


@pytest.mark.asyncio
async def test_cancel_schedule_should_raise_schedule_not_found_when_exception_is_raised(mocker, mock_logging):
    mock_client = mocker.patch("app.utils.schedule.client", autospec=True)
    mock_client.delete_schedule.side_effect = Exception("Error")
    mock_client.exceptions.ResourceNotFoundException = Exception

    with pytest.raises(ScheduleNotFound):
        await cancel_schedule("arn")

    mock_logging.info.assert_called_once()


@pytest.mark.asyncio
async def test_cancel_schedule_should_log_error_when_exception_is_raised(mocker, mock_logging):
    mock_client = mocker.patch("app.utils.schedule.client", autospec=True)

    mock_client.delete_schedule.side_effect = Exception("Error")
    mock_client.exceptions.ResourceNotFoundException = ValueError

    await cancel_schedule("arn")

    mock_logging.error.assert_called_once()


@pytest.mark.asyncio
async def test_cancel_schedule_should_return_none_when_schedule_is_deleted(mocker, mock_logging):
    mock_client = mocker.patch("app.utils.schedule.client", autospec=True)
    mock_client.delete_schedule.return_value = None

    assert await cancel_schedule("arn") is None
