from sqlmodel import Session, select, delete
from sqlalchemy.orm import selectinload
import httpx
from fastapi import BackgroundTasks
from app.models import Container

class ContainerManager:
    
    async def send_agent_request(address, method, endpoint):
        try:
            url = f"http://{address}:8001/{endpoint}"
            print('sending reqquest to', url)
            async with httpx.AsyncClient() as client:
                response = await client.request(method=method, url=url, data={})
                print("agent respsone", response)
                response.raise_for_status()
        except Exception as e:
            print(f'agent request error: {str(e)}')
            return None
    
    def create():
        return NotImplementedError
    
    def start(id, session: Session, background_tasks: BackgroundTasks):
        statement = select(Container).where(Container.id == id).options(selectinload(Container.machine))
        container = session.exec(statement).one_or_none()
        if not container:
            return None
        
        # send request to agent at target address /docker/{id}/start
        background_tasks.add_task(
            ContainerManager.send_agent_request,
            address=container.machine.tailscale_ip,
            method="POST",
            endpoint=f"containers/{container.docker_id}/start",
        )
        # return ok or something
        return {"status": "accepted"}
        
    
    def stop(id, session: Session, background_tasks: BackgroundTasks):
        statement = select(Container).where(Container.id == id).options(selectinload(Container.machine))
        container = session.exec(statement).one_or_none()
        if not container:
            return None
        
        # send request to agent at target address /docker/{id}/stop
        background_tasks.add_task(
            ContainerManager.send_agent_request,
            address=container.machine.tailscale_ip,
            method="POST",
            endpoint=f"containers/{container.docker_id}/stop",
        )
        # return ok or something
        return {"status": "accepted"}
    
    def delete(id):
        return NotImplementedError
    
    
    