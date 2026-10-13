from fastapi import APIRouter, HTTPException
import httpx
from sqlmodel import Session, select, delete
from typing import Dict, Any
from pydantic import BaseModel
from app.core.responses import response_template
from app.dependencies import get_session
from app.features.agent.manager import AgentManager
from app.models import Machine

router = APIRouter(
    prefix="/agents",
    tags=["agents"]
)


from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.orm import Session

@router.post("/update")
async def update_agent(
    data: Dict[str, Any], 
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session)
):
    machine_id = data.get("id")
    if not machine_id:
        return response_template(400, "Invalid Machine ID provided")

    machine = session.exec(select(Machine).where(Machine.id == machine_id)).one_or_none()
    if not machine:
        return response_template(404, f"Machine with ID {machine_id} not found")

    try:
        # 3. Queue the heavy Paramiko update to run in the background 
        # so it doesn't freeze the FastAPI event loop or block the HTTP response
        background_tasks.add_task(AgentManager.update, machine)

        return response_template(
            200, 
            "Update triggered successfully", 
            {"status": "updating", "machine_id": machine.id}
        )
        
    except Exception as e:
        return response_template(500, f"Failed to initiate update: {str(e)}")
