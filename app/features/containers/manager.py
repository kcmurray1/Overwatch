from sqlmodel import Session, select, delete
from sqlalchemy.orm import selectinload
import httpx
import docker
from fastapi import BackgroundTasks
from app.models import Container
from .utils import ContainerUtils

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
        
    @staticmethod   
    def detect_existing_containers(machine_obj, session:Session):
        """use DockerClient to gather existing containers on machine\n
            :NOTE: This will not function if the target device and client device do not have
            SSH authentication setup
        """
        print(f"connecting to ssh://{machine_obj.user}@{machine_obj.address}:{machine_obj.port}")
        docker_client = docker.DockerClient(base_url=f"ssh://{machine_obj.user}@{machine_obj.address}:{machine_obj.port}", use_ssh_client=True, version='auto', 
        timeout=60)
        containers_to_add = []
        for container in docker_client.containers.list(all=True):
            container_info = container.attrs
            ContainerUtils.get_url(container_info)
            containers_to_add.append(Container(
                docker_id=container_info.get("Id"),
                image=container_info["Config"]["Image"],
                name=container_info.get("Name","").lstrip("/"),
                config=container_info,
                state=container_info["State"]["Status"],
                machine_id=machine_obj.id,
            ))
            
        session.add_all(containers_to_add)
        session.commit()

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
    
    
    