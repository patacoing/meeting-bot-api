import pytest

from app.exceptions import BadRequestSignature
from app.utils.verification import verif, MissingRequestBody


@pytest.fixture
def mock_logging(mocker):
    return mocker.patch("app.utils.verification.logger", autospec=True)


@pytest.fixture
def mock_request(mocker):
    mock_request = mocker.MagicMock()
    mock_request.body = mocker.AsyncMock(return_value=b'{"key": "value"}')
    mock_request.headers = {
        "X-Signature-Ed25519": "0123456789abcdef",
        "X-Signature-Timestamp": "timestamp",
    }
    return mock_request


@pytest.mark.asyncio
async def test_verif_should_raise_missing_request_body_when_body_is_empty(mocker, mock_logging):
    mock_request = mocker.MagicMock()
    mock_request.body = mocker.AsyncMock(return_value=b"")

    with pytest.raises(MissingRequestBody):
        await verif(mock_request)


@pytest.mark.asyncio
async def test_verif_should_raise_bad_request_signature_when_verify_key_is_not_valid(mocker, mock_logging,
                                                                                     mock_request):
    mocker.patch("app.utils.verification.verify_key", autospec=True, return_value=False)

    with pytest.raises(BadRequestSignature):
        await verif(mock_request)

    mock_logging.info.assert_called_once()


@pytest.mark.asyncio
async def test_verif_should_raise_bad_request_signature_when_signature_is_none(mocker, mock_logging, mock_request):
    mock_request.headers = {
        "X-Signature-Ed25519": "0123456789abcdef",
    }

    mocker.patch("app.utils.verification.verify_key", autospec=True, return_value=False)

    with pytest.raises(BadRequestSignature):
        await verif(mock_request)

    mock_logging.info.assert_called_once()


@pytest.mark.asyncio
async def test_verif_should_raise_bad_request_signature_when_signature_is_none(mocker, mock_logging, mock_request):
    mock_request.headers = {
        "X-Signature-Timestamp": "timestamp",
    }

    mocker.patch("app.utils.verification.verify_key", autospec=True, return_value=False)

    with pytest.raises(BadRequestSignature):
        await verif(mock_request)

    mock_logging.info.assert_called_once()


@pytest.mark.asyncio
async def test_verif_should_not_raise_exception_when_request_is_valid(mocker, mock_logging, mock_request):
    mocker.patch("app.utils.verification.verify_key", autospec=True, return_value=True)

    assert await verif(mock_request) is None
    mock_logging.info.assert_not_called()
