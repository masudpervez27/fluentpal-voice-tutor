import logging

from fastapi import APIRouter, HTTPException

from ..models.schemas import (
    StartSessionRequest,
    StartSessionResponse,
    TutorTurnRequest,
    TutorTurnResponse,
)
from ..services.tutor import process_turn, start_session

router = APIRouter(prefix="/api")
logger = logging.getLogger(__name__)


@router.get("/health")
async def health():
    logger.info("Health endpoint called")
    return {"status": "ok"}


@router.post("/session")
async def create_session(payload: StartSessionRequest) -> StartSessionResponse:
    logger.info("Session endpoint called for learner=%s", payload.learner_name)
    return start_session(payload)


@router.post("/turn")
async def tutor_turn(payload: TutorTurnRequest) -> TutorTurnResponse:
    logger.info("Turn endpoint called for session=%s", payload.session_id)
    try:
        return process_turn(payload.session_id, payload.transcript)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
