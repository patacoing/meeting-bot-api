from fastapi import FastAPI, Depends
from mangum import Mangum

from app.schemas import DiscordRequest, DiscordType, DiscordResponse, Command, DiscordResponseData
from app.utils.verification import verif
from app.utils.operation import plan_meeting, cancel_meeting
from app.utils.logging import logger

app = FastAPI()


@app.post(
    "/",
    dependencies=[Depends(verif)],
)
async def read_root(request: DiscordRequest):
    if request.type == DiscordType.PING:
        logger.debug("Received PING")
        response_data = DiscordResponse(type=DiscordType.PONG)
    else:
        data = request.data
        command_name = data.name

        if command_name == Command.PLAN:
            logger.debug("Received PLAN command")
            message_content = await plan_meeting(data)
        elif command_name == Command.CANCEL:
            logger.debug("Received CANCEL command")
            message_content = await cancel_meeting(data)
        else:
            message_content = "Unknown command"
            logger.info(f"Unknown command: {command_name}")

        response_data = DiscordResponse(
            type=DiscordType.RESPONSE,
            data=DiscordResponseData(content=message_content)
        )

    return response_data.dict(exclude_none=True)


handler = Mangum(app, lifespan="off")
