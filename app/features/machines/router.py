from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session, selectinload
from pydantic import BaseModel
from sqlmodel import select
from typing import Optional
from app.dependencies import get_session
from app.models import Machine, MachineBase
from .manager import MachineManager
from app.config import Settings, get_settings
from app.core.responses import response_template
from app.features.containers.manager import ContainerUtils
router = APIRouter(
    prefix="/machines",
    tags=["machines"]
)



@router.get("")
async def list_machines(
    include: Optional[str] = Query(None),
    session: Session = Depends(get_session)
    ):
    # Standard SQLAlchemy syntax
    machines = session.execute(select(Machine).options(selectinload(Machine.containers))).scalars().all()

    data = []
    for machine in machines:
        machine_dict = machine.model_dump()
        container_data = []
        for container in machine.containers:
            container_dict = container.model_dump()
            container_dict["primary_url"] = ContainerUtils.get_url(container_dict["config"], machine.tailscale_ip)
            container_data.append(container_dict)
        machine_dict["containers"] = container_data
        
        data.append(machine_dict)

    return response_template(status=200, message="ok", data=data)

@router.post("")
async def add_machine(payload: MachineBase, session: Session = Depends(get_session), settings: Settings = Depends(get_settings)):   
    new_machine = MachineManager.add_machine(
        payload.address, 
        payload.port, 
        payload.user, 
        keypath=settings.key_path,
        session=session
    )
    return response_template(status=201, message="created", data=new_machine)

@router.delete("/{id}")
async def delete_machine(id, session: Session = Depends(get_session)):
    MachineManager.remove_machine(id, session)
    return response_template(200, "ok")


@router.get("/{id}/usage")
async def get_usage(id, session: Session = Depends(get_session)):
    data = MachineManager.get_usage(id, session)
    if not data:
        return response_template(status=404, message='agent not responding')
    return response_template(status=200, message='ok', data=data)

@router.post("/{id}/openvs")
async def open_vscode(id, session: Session = Depends(get_session)):
    URI = MachineManager.open_vscode(id, session)
    return response_template(status=200, message="ok", data={'link': URI})

import asyncio

@router.post("/scan")
async def scan_machine_connections(session: Session = Depends(get_session)):
    db_machines = session.exec(select(Machine)).all()
    
    # Convert ORM objects to plain dicts so threads don't touch active session instances
    target_data = [{"id": m.id, "user": m.user, "port": m.port} for m in db_machines]
    await asyncio.to_thread(MachineManager.scan_network, target_data)
    
    return response_template(status=200, message="Subnet scan complete")

