from fastapi import APIRouter, Depends, BackgroundTasks
from sqlmodel import Session, select, delete
from typing import Dict, Any
from pydantic import BaseModel
from app.dependencies import get_session
from app.models import Container
from app.extensions import docker_orchestrator
from app.core.responses import response_template
from .manager import ContainerManager
from .schemas import ContainerConfig
router = APIRouter(
    prefix="/containers",
    tags=["containers"]
)


@router.get("")
def read_containers(session: Session = Depends(get_session)):
    containers = ContainerManager.list_containers(session)
    return response_template(status=200, message="ok", data=containers)

@router.post("")
def create_container(project_data: Dict[str, Any], session:Session = Depends(get_session)):
    new_container = docker_orchestrator.add_container(session,**project_data)

    return response_template(200, "ok", new_container)

# @router.get("/{id}")
# async def read_container(id, session: Session = Depends(get_session)):
#     project = docker_orchestrator.get_(id, session=session)

#     return response_template(200, "ok", project)

@router.delete("/{id}")
async def delete_container(id, session: Session = Depends(get_session)):
    removed_project = docker_orchestrator.remove_container(id, session)

    return response_template(200, "ok", removed_project)

@router.post("/{id}/start")
async def start_container(
    id, 
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session)):
    print('starting container..', id)
    ContainerManager.start(id, session, background_tasks)
    return response_template(200, "ok")

@router.post("/{id}/stop")
async def stop_container( id, 
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session)):
    print('stopping container..', id)
    ContainerManager.stop(id, session, background_tasks)
    print("stopping container", id)
    
    return response_template(200, "ok")


class DockerActionType:
    START = "start" # connect, start
    DESTROY = "destroy"
    STOP = "stop" # kill, disconnect, stop, die
    DIE = "die"
    

class DockerEvent(BaseModel):
    action: str
    container_id: str
    host_address: str
    attrs: Dict[str, Any]
                

@router.post("/event")
async def update_container(data: DockerEvent, session: Session = Depends(get_session)):
    action = data.action
    container_id = data.container_id
    print(data.attrs)
    container = session.exec(select(Container).where(Container.docker_id == container_id)).one_or_none()
    if not container:
        return
    
    if action == DockerActionType.DESTROY:
        print("removing container")
        session.delete(container)
    elif action == DockerActionType.START:
        print("starting container")
        container.state = "running"
        
    elif action == DockerActionType.STOP or action == DockerActionType.DIE:
        print("stopping container")
        container.state = "offline"
    else:
        print("unsupported docker action type", action)
    
    session.commit()
    

    return {"status": "ok"}


@router.get("/configs")
def read_container_configs(session: Session = Depends(get_session)):
    configs = ContainerManager.list_configs(session)
    
    return response_template(status=200, message="ok", data=configs)

@router.post("/deploy")
def deploy_container(
    data: Dict[str, Any], 
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session),
    ):
    
    machines = data.pop("machines")
    
    ContainerManager.create(machines, data, background_tasks)
    
    
    
    print(data)
    
    return response_template(201, "created")