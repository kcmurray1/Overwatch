from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import StreamingResponse
import docker
from docker.errors import APIError, NotFound

router = APIRouter(
    prefix="/containers",
    tags=["containers"]
)

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


@router.post("/{container_id}/start")
def start_container(
    container_id: str,
    client: docker.DockerClient = Depends(get_docker_client)
):
    """Start a container by ID or Name."""
    try:
        container = client.containers.get(container_id)
        container.start()
        return {"status": "success", "message": f"Container {container_id} started"}
    except NotFound:
        raise HTTPException(status_code=404, detail=f"Container '{container_id}' not found")
    except APIError as e:
        raise HTTPException(status_code=500, detail=str(e))


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
