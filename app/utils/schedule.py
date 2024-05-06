import boto3

from app.exceptions import ScheduleNotFound
from app.schemas import EventBridgeRequest, EventBridgeAction
from app.settings import settings
from app.utils.logging import logger

client = boto3.client('scheduler', region_name=settings.AWS_REGION)


async def schedule(
        name: str,
        description: str,
        year: int,
        month: str,
        day: str,
        hour: str,
        minute: str
) -> None:
    try:
        arn = client.create_schedule(
            ActionAfterCompletion="DELETE",
            Description=description,
            FlexibleTimeWindow={
                "Mode": "FLEXIBLE",
                "MaximumWindowInMinutes": 1,
            },
            Name=name,
            ScheduleExpression=f"at({year}-{month}-{day}T{hour}:{minute}:00)",
            Target={
                "Arn": settings.CALLBACK_SCHEDULE_ARN,
                "RoleArn": settings.ROLE_ARN,
                "Input": EventBridgeRequest(
                    action=EventBridgeAction.PING,
                    name=name,
                    time=f"{hour}:{minute}",
                    description=description,
                ).json(
                )
            },
        )
        logger.info(f"ARN : {arn.get('ScheduleArn', '')}")
    except Exception as ex:
        logger.error(ex)


async def cancel_schedule(name: str) -> None:
    try:
        client.delete_schedule(Name=name)
    except client.exceptions.ResourceNotFoundException:
        logger.info(f"Schedule {name} not found")
        raise ScheduleNotFound(name)
    except Exception as ex:
        logger.error(ex)
