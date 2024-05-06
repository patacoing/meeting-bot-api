from app.exceptions import InvalidFieldsCount
from app.utils.logging import logger


def parse_fields(length: int, separator: str, data: str, convert: callable = str) -> list:
    fields = data.split(separator)
    if len(fields) != length:
        logger.info("Invalid fields count")
        raise InvalidFieldsCount()
    return list(map(convert, fields))
