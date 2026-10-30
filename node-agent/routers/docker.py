from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import StreamingResponse
import docker
from typing import Dict, Any
from docker.errors import APIError, NotFound
import logging
router = APIRouter(
    prefix="/containers",
    tags=["containers"]
)
logger = logging.getLogger(__name__)

def get_docker_client():
    """Dependency provider for Docker SDK client."""
    try:
        return docker.from_env()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Could not connect to local Docker daemon: {str(e)}"
        )


@router.get("/{container_id}")
def get_container(
    container_id: str,
    client: docker.DockerClient = Depends(get_docker_client)
):
    """Get inspect attributes for a specific container."""
    try:
        container = client.containers.get(container_id)
        return container.attrs
    except NotFound:
        raise HTTPException(status_code=404, detail=f"Container '{container_id}' not found")
    except APIError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/create")
def create_container(
    data: Dict[str, Any],
    client: docker.DockerClient = Depends(get_docker_client)
):
    try:
        logger.info(data)
        if "ports" in data and isinstance(data["ports"], dict):
            normalized_ports = {}
            logger.info("normalizing ports")
            for container_port, binding in data["ports"].items():
                # If the JSON parsed a host/port binding as a list, convert it to a tuple for Docker SDK
                normalized_ports[container_port] = tuple(binding.split(':'))
                    
            data["ports"] = normalized_ports

        container = client.containers.create(**data)
        
        return {"status": "success", "message": f"Container {container.id} created"}
    except Exception as e:
        logger.error(f'Container Start Error: {str(e)}')
        raise HTTPException(status_code=404, detail=f"Container unable to be created")



@router.post("/{container_id}/start")
def start_container(
    container_id: str,
    client: docker.DockerClient = Depends(get_docker_client)
):
    logger.info(f'starting container: {container_id}')
    try:
        container = client.containers.get(container_id)
        container.start()
        return {"status": "success", "message": f"Container {container_id} started"}
    except Exception as e:
        logger.error(f'Container Start Error: {str(e)}')
        raise HTTPException(status_code=404, detail=f"Container '{container_id}' not found")


@router.post("/{container_id}/stop")
def stop_container(
    container_id: str,
    timeout: int = Query(default=10, description="Seconds to wait before killing"),
    client: docker.DockerClient = Depends(get_docker_client)
):
    try:
        container = client.containers.get(container_id)
        container.stop(timeout=timeout)
        return {"status": "success", "message": f"Container {container_id} stopped"}
    except NotFound:
        raise HTTPException(status_code=404, detail=f"Container '{container_id}' not found")
    except APIError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{container_id}/restart")
def restart_container(
    container_id: str,
    timeout: int = Query(default=10, description="Seconds to wait before killing during restart"),
    client: docker.DockerClient = Depends(get_docker_client)
):
    try:
        container = client.containers.get(container_id)
        container.restart(timeout=timeout)
        return {"status": "success", "message": f"Container {container_id} restarted"}
    except NotFound:
        raise HTTPException(status_code=404, detail=f"Container '{container_id}' not found")
    except APIError as e:
        raise HTTPException(status_code=500, detail=str(e))
