from fastapi import APIRouter
import logging
router = APIRouter(
    prefix="/agent",
    tags=["agent"]
)

logger = logging.getLogger(__name__)

@router.get("/")
def agent_status(container_id: str):
    return {"status": "agent status is running"}