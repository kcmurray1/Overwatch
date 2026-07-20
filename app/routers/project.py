from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends
from sqlmodel import Session, select, delete
from app.dependencies import get_session
from app.models_fast.model import Container, ContainerBase
from app.extensions import docker_orchestrator
from typing import Dict, Any
def response_template(status: int, message: str, data=None):
    return JSONResponse(
        status_code=status,
        content={"message": message, "data": data}
    )

router = APIRouter(
    prefix="/containers",
    tags=["containers"]
)


@router.get("/")
def read_containers(session: Session = Depends(get_session)):
    containers = docker_orchestrator.get_containers(session)
    return response_template(status=200, message="ok", data=containers)

@router.post("/")
def create_container(project_data: Dict[str, Any], session:Session = Depends(get_session)):
    new_container = docker_orchestrator.add_container(session,**project_data)

    return response_template(200, "ok", new_container)

@router.get("/{id}")
async def read_container(id, session: Session = Depends(get_session)):
    project = docker_orchestrator.get_(id, session=session)

    return response_template(200, "ok", project)

@router.delete("/{id}")
async def delete_container(id, session: Session = Depends(get_session)):
    removed_project = docker_orchestrator.remove_container(id, session)

    return response_template(200, "ok", removed_project)

@router.post("/{id}/actions")
async def change_container_state(id, payload, session: Session = Depends(get_session)):
    action = payload.get("action")
    
    if not action:
        print("throw error accion")
        pass
    
    if action == "start":
        pass
    elif action == "stop":
        pass
    else:
        print("unsupported action", action)
        
    return response_template(200, "ok")