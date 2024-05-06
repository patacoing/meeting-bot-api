from fastapi import HTTPException, status


class InvalidOptionsCount(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid options count")


class ScheduleNotFound(HTTPException):
    def __init__(self, name: str):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=f"Schedule {name} not found")


class MissingRequestBody(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing request body")


class BadRequestSignature(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail="Bad request signature")


class InvalidFieldsCount(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid fields count")
