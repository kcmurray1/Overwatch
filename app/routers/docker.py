from fastapi import APIRouter, Depends
from app.dependencies import get_session
from sqlmodel import Session
from typing import Dict, Any
from pydantic import BaseModel
router = APIRouter(
    prefix="/docker",
    tags=["docker"]
)


class DockerEvent(BaseModel):
    Type: str
    Action: str
    Actor: Dict[str, Any]


@router.post("/event")
async def update_event(data: DockerEvent, session: Session = Depends(get_session)):
    if data.Type == 'container1':
        # update list of containers based on data.Action(start, connect, kill,destroy, etc)

        # get basic image information of container(name, image, id)
        attributes = data.Actor['Attributes']
        for attr in attributes:
            print(attributes[attr])

    return {"status": "ok"}

@router.post("/")
async def create_container(data, session: Session = Depends(get_session)):

    pass