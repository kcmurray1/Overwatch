from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends
from sqlmodel import Session, select, delete
from app.dependencies import get_session
from app.extensions import docker_orchestrator
def response_template(status: int, message: str, data=None):
    return JSONResponse(
        status_code=status,
        content={"message": message, "data": data}
    )

router = APIRouter(
    prefix="/blueprints",
    tags=["blueprints"]
)


@router.get("/")
def read_blueprints(session: Session = Depends(get_session)):
    
    blueprints = docker_orchestrator.get_blueprints()

    
    return response_template(status=200, message="ok", data=blueprints)