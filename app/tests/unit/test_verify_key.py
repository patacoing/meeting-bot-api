import pytest
from app.utils.verification import verify_key


@pytest.fixture
def mock_logging(mocker):
    return mocker.patch("app.utils.verification.logger", autospec=True)


def test_verify_key_should_return_false_when_signature_is_invalid(mocker, mock_logging):
    mock_verify_key = mocker.patch("app.utils.verification.VerifyKey", autospec=True)
    mock_verify_key.return_value.verify.side_effect = Exception("Invalid signature")

    mock_settings = mocker.patch("app.utils.verification.settings", autospec=True)
    mock_settings.CLIENT_PUBLIC_KEY = "0123456789abcdef"

    raw_body = b'{"key": "value"}'
    signature = 'invalid_signature'
    timestamp = 'timestamp'

    assert verify_key(raw_body, signature, timestamp) is False
    mock_logging.error.assert_called_once()


def test_verify_key_should_return_true_when_signature_is_valid(mocker, mock_logging):
    mock_verify_key = mocker.patch("app.utils.verification.VerifyKey", autospec=True)
    mock_verify_key.return_value.verify.return_value = None

    mock_settings = mocker.patch("app.utils.verification.settings", autospec=True)
    mock_settings.CLIENT_PUBLIC_KEY = "0123456789abcdef"

    raw_body = b'{"key": "value"}'
    signature = '0123456789abcdef'
    timestamp = 'timestamp'

    assert verify_key(raw_body, signature, timestamp) is True
    mock_logging.error.assert_not_called()
