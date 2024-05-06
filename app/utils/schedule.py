import boto3
from app.settings import settings
from json import dumps
from fastapi import HTTPException, status
from app.utils.logging import logger

client = boto3.client('scheduler', region_name=settings.AWS_REGION)


async def schedule(name: str, description: str, year: str, month: str, day: str, hour: str, minute: str) -> None:
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
                "Input": dumps({
                    "action": "ping",
                    "name": name,
                    "time": f"{hour}:{minute}",
                    "description": description,
                })
            },
        )
        logger.info(f"ARN : {arn.get('ScheduleArn', '')}")
    except Exception as ex:
        logger.error(ex)


async def cancel_schedule(name: str) -> None:
    try:
        client.delete_schedule(
            Name=name
        )
    except client.exceptions.ResourceNotFoundException:
        logger.info(f"Schedule {name} not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Schedule {name} not found")
    except Exception as ex:
        logger.error(ex)
