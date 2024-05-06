import pytest

from app.exceptions import InvalidFieldsCount
from app.utils.parse import parse_fields


@pytest.fixture
def mock_logging(mocker):
    return mocker.patch("app.utils.parse.logger", autospec=True)


def test_parse_fields_should_raise_invalid_fields_count_when_fields_count_is_not_valid(mock_logging):
    with pytest.raises(InvalidFieldsCount):
        parse_fields(
            length=2,
            separator=",",
            data="field1,field2,field3",
            convert=str,
        )

    mock_logging.info.assert_called_once()


@pytest.mark.parametrize(
    "length, separator, data, convert, expected",
    [
        (2, ",", "field1,field2", str, ["field1", "field2"]),
        (2, ".", "field1.field2", str, ["field1", "field2"]),
        (2, "-", "field1-field2", str, ["field1", "field2"]),
        (2, " ", "field1 field2", str, ["field1", "field2"]),
        (2, ",", "1,2", int, [1, 2]),
        (2, ".", "1.2", int, [1, 2]),
        (2, "-", "1-2", int, [1, 2]),
        (2, " ", "1 2", int, [1, 2]),
    ],
)
def test_parse_fields_should_return_list_of_fields_when_fields_count_is_valid(mock_logging, length, separator, data,
                                                                              convert, expected):
    assert parse_fields(
        length=length,
        separator=separator,
        data=data,
        convert=convert,
    ) == expected
