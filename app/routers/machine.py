from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_session
# from app.models_fast.machine import Machine, MachineBase
from app.models_fast.model import Machine, MachineBase
from app.machine_manager import MachineManager
# from app.core.errors import APIError, response_template
from app.config import Settings, get_settings
from pydantic import BaseModel
from sqlmodel import select
router = APIRouter(
    prefix="/machines",
    tags=["machines"]
)


def response_template(status, message, data=None):
    return {"message": message, "data": data}

@router.get("/")
async def list_machines(session: Session = Depends(get_session)):
    # Standard SQLAlchemy syntax
    machines = session.execute(select(Machine)).scalars().all()

    machines = [machine.model_dump() for machine in machines]

    return response_template(status=200, message="ok", data=machines)

@router.post("/")
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

