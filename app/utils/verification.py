from fastapi import Request, HTTPException, status
from nacl.signing import VerifyKey
from app.settings import settings
from app.utils.logging import logger


def verify_key(raw_body: bytes, signature: str, timestamp: str) -> bool:
    verify_key = VerifyKey(bytes.fromhex(settings.CLIENT_PUBLIC_KEY))

    try:
        verify_key.verify(f'{timestamp}{raw_body}'.encode(), bytes.fromhex(signature))
        return True
    except Exception as ex:
        logger.error(ex)
    return False


async def verif(request: Request):
    if settings.DEBUG:
        return

    signature = request.headers.get("X-Signature-Ed25519")
    timestamp = request.headers.get("X-Signature-Timestamp")
    body = (await request.body()).decode("utf-8")

    if not body:
        logger.info("Missing request body")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing request body")

    if signature is None or timestamp is None or not verify_key(body, signature, timestamp):
        logger.info("Bad request signature")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Bad request signature")
