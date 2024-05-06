from datetime import datetime
from uuid import uuid4
from .schedule import schedule, cancel_schedule
from .parse import parse_fields
from app.utils.logging import logger
from ..exceptions import InvalidOptionsCount
from ..schemas import DiscordRequestData, OptionName, DATE_SEPARATOR, TIME_SEPARATOR


async def plan_meeting(data: DiscordRequestData) -> str:
    if len(data.options) != 3:
        logger.info("Invalid options count")
        raise InvalidOptionsCount()

    name = f'meeting-{uuid4()}'
    date = time = description = None

    for option in data.options:
        if option.name == OptionName.DATE:
            date = option.value
        elif option.name == OptionName.TIME:
            time = option.value
        elif option.name == OptionName.DESCRIPTION:
            description = option.value

    day, month = parse_fields(2, DATE_SEPARATOR, date)
    hour, minute = parse_fields(2, TIME_SEPARATOR, time)
    year = datetime.now().year

    await schedule(
        name,
        description,
        year=year,
        month=month,
        day=day,
        hour=hour,
        minute=minute
    )

    logger.info(f"Meeting {name} planned for {date} at {time} - {description}")
    return f"Meeting {name} planned for {date} at {time} - {description}"


async def cancel_meeting(data: DiscordRequestData) -> str:
    if len(data.options) != 1:
        logger.info("Invalid options count")
        raise InvalidOptionsCount()

    name = data.options[0].value

    await cancel_schedule(name)

    logger.info(f"Meeting {name} cancelled")
    return f"Meeting {name} cancelled"
