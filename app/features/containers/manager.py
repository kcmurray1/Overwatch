from sqlmodel import Session, select, delete
from sqlalchemy.orm import selectinload
import httpx
import docker
from fastapi import BackgroundTasks
from app.models import Container
from .utils import ContainerUtils
from .schemas import ContainerConfig
class ContainerManager:
    
    async def send_agent_request(address, method, endpoint, data={}):
        try:
            url = f"http://{address}:8001/{endpoint}"
            print('sending reqquest to', url)
            async with httpx.AsyncClient() as client:
                response = await client.request(method=method, url=url, json=data)
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

    def create(machine_objects, config, background_tasks: BackgroundTasks):
        for machine_object in machine_objects:
            background_tasks.add_task(
                ContainerManager.send_agent_request,
                address=machine_object.get("address"),
                method="POST",
                endpoint=f"containers/create",
                data=config
            )
            
        
        
        
    
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
    
    def restart(id, session: Session, background_tasks: BackgroundTasks):
        container = session.exec(select(Container).where(Container.id == id).options(selectinload(Container.machine))).one_or_none()
        if not container:
            return "Container does not exist"
        
        background_tasks.add_task(
            ContainerManager.send_agent_request,
            address=container.machine.tailscale_ip,
            method="POST",
            endpoint=f"containers/{container.docker_id}/restart"
        )
        return "accepted"
    
    def delete(id, session: Session, background_tasks: BackgroundTasks):
        container = session.get(Container, id)
        if not container:
           return "Container does not exist"

        # 2. Queue the background request to the agent using the fetched relationship
        background_tasks.add_task(
            ContainerManager.send_agent_request,
            address=container.machine.tailscale_ip,
            method="DELETE",
            endpoint=f"containers/{container.docker_id}" # or container.name depending on what your agent expects
        )

        # 3. Delete the record from the control plane DB in one lookup
        session.delete(container)
        session.commit()
    
    
    def list_containers(session: Session):
        containers = session.exec(select(Container)).all()
        return [container.model_dump() for container in containers]
    
    
    def list_configs(session: Session):
        configs = session.exec(select(ContainerConfig)).all()
        from fastapi.encoders import jsonable_encoder
        return [jsonable_encoder(config.model_dump()) for config in configs]
    
    