from datetime import datetime
from fastapi import HTTPException, status
from uuid import uuid4
from .schedule import schedule, cancel_schedule
from .parse import parse_fields
from app.utils.logging import logger


async def plan_meeting(data: dict) -> str:
    if len(data["options"]) != 3:
        logger.info("Invalid options count")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid options count")

    name = f'meeting-{uuid4()}'
    for option in data["options"]:
        if option["name"] == "date":
            date = option["value"]
        elif option["name"] == "time":
            time = option["value"]
        elif option["name"] == "description":
            description = option["value"]

    day, month = parse_fields(2, "/", date)
    hour, minute = parse_fields(2, ":", time)
    year = datetime.now().year

    await schedule(name, description, year=year, month=month, day=day, hour=hour, minute=minute)

    logger.info(f"Meeting {name} planned for {date} at {time} - {description}")
    return f"Meeting {name} planned for {date} at {time} - {description}"


async def cancel_meeting(data: dict) -> str:
    if len(data["options"]) != 1:
        logger.info("Invalid options count")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid options count")

    name = data["options"][0]["value"]

    await cancel_schedule(name)

    logger.info(f"Meeting {name} cancelled")
    return f"Meeting {name} cancelled"
