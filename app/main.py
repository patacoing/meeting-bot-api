from fastapi import FastAPI, Depends, Request
from mangum import Mangum
from app.utils.verification import verif
from app.utils.operation import plan_meeting, cancel_meeting
from app.utils.logging import logger

app = FastAPI()


@app.post(
    "/",
    dependencies=[Depends(verif)],
)
async def read_root(request: Request):
    content = await request.json()

    if content["type"] == 1:  # PING
        logger.debug("Received PING")
        response_data = {"type": 1}  # PONG
    else:
        data = content["data"]
        command_name = data["name"]

        if command_name == "plan":
            logger.debug("Received PLAN command")
            message_content = await plan_meeting(data)
        elif command_name == "cancel":
            logger.debug("Received CANCEL command")
            message_content = await cancel_meeting(data)
        else:
            message_content = "Unknown command"
            logger.info(f"Unknown command: {command_name}")

        response_data = {
            "type": 4,
            "data": {"content": message_content},
        }
    return response_data


handler = Mangum(app, lifespan="off")
