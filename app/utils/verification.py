from fastapi import Request
from nacl.signing import VerifyKey

from app.exceptions import BadRequestSignature, MissingRequestBody
from app.settings import settings
from app.utils.logging import logger


def verify_key(raw_body: bytes, signature: str, timestamp: str) -> bool:
    verified_key = VerifyKey(bytes.fromhex(settings.CLIENT_PUBLIC_KEY))

    try:
        verified_key.verify(f'{timestamp}{raw_body}'.encode(), bytes.fromhex(signature))
        return True
    except Exception as ex:
        logger.error(ex)
    return False


async def verif(request: Request):
    if settings.DEBUG:
        return

    signature = request.headers.get("X-Signature-Ed25519")
    timestamp = request.headers.get("X-Signature-Timestamp")
    body = await request.body()

    if not body:
        logger.info("Missing request body")
        raise MissingRequestBody()

    if signature is None or timestamp is None or not verify_key(body, signature, timestamp):
        logger.info("Bad request signature")
        raise BadRequestSignature()
