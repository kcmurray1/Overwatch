from fastapi import APIRouter, Depends, BackgroundTasks, Request
from sqlmodel import Session, select, delete
from typing import Dict, Any
from pydantic import BaseModel

import logging
logger = logging.getLogger(__name__)


from app.core.configs.db import get_session
from app.models import Container, Machine
from app.features.machines.manager import MachineManager
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
    new_container = ContainerManager.create(session, **project_data)

    return response_template(200, "ok", new_container)

@router.patch("/{id}")
async def update_container(
    id: int,
    container_update: dict,
    session: Session = Depends(get_session)
):
    db_container = session.get(Container, id)
    db_container.sqlmodel_update(container_update)
    
    session.add(db_container)
    session.commit()
    session.refresh(db_container)

    return db_container

@router.delete("/{id}")
async def delete_container(
    id,
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session)):
    ContainerManager.delete(id, session, background_tasks)

    return response_template(200, "ok")

@router.post("/{id}/start")
async def start_container(
    id, 
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session)):
    logger.info(f'starting container.. {id}')
    ContainerManager.start(id, session, background_tasks)
    return response_template(200, "ok")

@router.post("/{id}/stop")
async def stop_container( id, 
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session)):
    logger.info(f'stopping container id:{id}')
    ContainerManager.stop(id, session, background_tasks)
    logger.info(f'stopped container id:{id}')
    
    return response_template(200, "ok")

@router.post("/{id}/restart")
async def restart_container(
    id,
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session)):
    result = ContainerManager.restart(id, session, background_tasks)
    return response_template(200, result)


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
async def update_container(data: DockerEvent, request: Request, session: Session = Depends(get_session)):
    action = data.action
    container_id = data.container_id

    logger.info(f'received docker action event: {data.action}')
    container = session.exec(select(Container).where(Container.docker_id == container_id)).one_or_none()
    if not container and action != DockerActionType.DESTROY and action != "kill":
        machine_obj = None
        local_address = request.client.host
        machine_obj = session.exec(select(Machine).where(Machine.tailscale_ip == local_address)).one_or_none()
        
        if not machine_obj:
            return {"status": "ignored", "reason": "machine not found"}
        if not data.attrs.get("State"):
            return {"status": "ignored", "reason": "state not found"}
        container = Container(
                docker_id=container_id,
                image=data.attrs.get("Image"),
                name=data.attrs.get("Name","").lstrip("/"),
                config=data.attrs,
                state=data.attrs["State"]["Status"],
                machine_id=machine_obj.id)
                    
        session.add(container)
    

    
    if action == DockerActionType.DESTROY and container:
        logger.info("docker action event: removing container")
        session.delete(container)
    elif action == DockerActionType.START:
        logger.info("docker action event: starting container")
        container.state = "running"
        
    elif action == DockerActionType.STOP or action == DockerActionType.DIE:
        logger.info("docker action event: stopping container")
        container.state = "offline"
    else:
        logger.info(f'docker action event: unsupported docker action type {action}')
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
    
    machine_ids = data.pop("machine_ids")
    MachineManager.deploy_container(machine_ids, data, session, background_tasks)
       
    return response_template(201, "created")