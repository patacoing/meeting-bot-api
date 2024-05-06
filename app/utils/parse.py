from fastapi import HTTPException, status
from app.utils.logging import logger


def parse_fields(length: int, separator: str, data: str, convert: callable = str) -> list:
    fields = data.split(separator)
    if len(fields) != length:
        logger.info("Invalid fields count")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid fields count")
    return list(map(convert, fields))
