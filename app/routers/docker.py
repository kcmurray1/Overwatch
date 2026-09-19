from fastapi import APIRouter, Depends
from app.dependencies import get_session
from sqlmodel import Session, select, delete
from typing import Dict, Any
from pydantic import BaseModel
from app.models_fast.model import Container
router = APIRouter(
    prefix="/docker",
    tags=["docker"]
)


class DockerActionType:
    START = "start" # connect, start
    DESTROY = "destroy"
    STOP = "stop" # kill, disconnect, stop, die
    

class DockerEvent(BaseModel):
    Type: str
    Action: str
    Actor: Dict[str, Any]


@router.post("/event")
async def update_event(data: DockerEvent, session: Session = Depends(get_session)):
    print(data)
    action = data.Action
    attributes = data.Actor.get('Attributes')
    container_id = data.Actor.get('ID')
    
    if action == DockerActionType.DESTROY:
        print("removing container")
        container = session.exec(select(Container).where(Container.docker_id == container_id)).one_or_none()    
        if container:
            session.delete(container)
            session.commit()
    elif action == DockerActionType.START:
        print("starting container")
    elif action == DockerActionType.STOP:
        print("stopping container")
    else:
        print("unsupported docker action type", action)
    

    return {"status": "ok"}

@router.post("/")
async def create_container(data, session: Session = Depends(get_session)):

    pass