
from typing import Annotated
from fastapi import APIRouter, Depends, Body


from core.config import get_settings
from schemas.schemas import Response, ForTranscrib
from services.transcrib_serv import init_transcrib

router = APIRouter()
config = get_settings()



@router.post(
    "/transcrib",
    response_model=Response
)
async def start_transcrib_api(
    message: Annotated[ForTranscrib, Body(description="Событие в кафку", title="Событие")],
) -> Response:
    result = await init_transcrib(message=message)
    return result
