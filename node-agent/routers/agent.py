from fastapi import APIRouter

router = APIRouter(
    prefix="/agent",
    tags=["agent"]
)

@router.get("/")
def agent_status(container_id: str):
    return {"status": "agent status is running"}