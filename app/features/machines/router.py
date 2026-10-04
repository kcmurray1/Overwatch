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
    # machines = session.execute(select(Machine)).scalars().all()
    machines = session.execute(select(Machine).options(selectinload(Machine.containers))).scalars().all()

    data = []
    for machine in machines:
        machine_dict = machine.model_dump()
        machine_dict["containers"] = [c.model_dump() for c in machine.containers]
        
        data.append(machine_dict)
    # machines = [machine.model_dump() for machine in machines]

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

