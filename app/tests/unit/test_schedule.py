import pytest

from app.utils.schedule import schedule


@pytest.fixture
def mock_logging(mocker):
    return mocker.patch("app.utils.schedule.logger", autospec=True)


@pytest.mark.asyncio
async def test_schedule_should_log_error_when_exception_is_raised(mocker, mock_logging):
    mock_client = mocker.patch("app.utils.schedule.client", autospec=True)
    mock_client.create_schedule.side_effect = Exception("Error")

    await schedule("name", "description", 2022, "01", "01", "00", "00")

    mock_logging.error.assert_called_once()


@pytest.mark.asyncio
async def test_schedule_should_log_arn_when_exception_is_not_raised(mocker, mock_logging):
    mock_client = mocker.patch("app.utils.schedule.client", autospec=True)
    mock_client.create_schedule.return_value = {"ScheduleArn": "arn"}

    await schedule("name", "description", 2022, "01", "01", "00", "00")

    mock_logging.info.assert_called_once_with("ARN : arn")
