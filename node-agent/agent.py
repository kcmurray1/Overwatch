import os
import threading
import docker
import requests
import socket
from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from routers import DockerRouter, SystemRouter, AgentRouter
from routers.system import UsageMonitor
from logger import setup_logging, get_logger

CONTROL_PLANE_HOST = None
setup_logging(logfile_name="agent_main")
logger = get_logger("main")


def watch_docker_events():
    global CONTROL_PLANE_HOST
    try:
        client = docker.from_env()  # Automatically picks up unix://var/run/docker.sock
        logger.info("Started watching local Docker events...")
        
       
        # This loop blocks and waits for events natively from the local socket
        for event in client.events(decode=True):
            container_id = event.get("Actor").get("ID")
                
            payload = {
                "action": event.get("Action", ""),
                "container_id": container_id,
                "host_address": socket.gethostname(),
                "attrs": None
            }
            
            try:
                payload["attrs"] = client.containers.get(container_id).attrs
                logger.info('docker event triggered')
            except Exception as e:
                logger.error("container get error", str(e))
            
            # send request to control plane host
            if CONTROL_PLANE_HOST:
                try:
                    logger.info(payload)
                    logger.info('sending host udpated!')
                    requests.post(f"http://{CONTROL_PLANE_HOST}:5000/containers/event", json=payload, timeout=3)
                except Exception as e:
                    logger.error(f"error sending event {e}")
                
    except Exception as e:
        logger.error(f"Docker event listener crashed: {e}")

def write_pid():
    pid = os.getpid()
    with open("agent.pid", "w") as f:
        f.write(str(pid))





# https://fastapi.tiangolo.com/advanced/events/#lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("starting agent...")
    write_pid()
    threading.Thread(target=watch_docker_events, daemon=True).start()
    UsageMonitor.start_background_monitor()
    yield
    logger.info("stopping agent....")



app = FastAPI(lifespan=lifespan)

app.include_router(SystemRouter)
app.include_router(AgentRouter)
app.include_router(DockerRouter)

@app.get("/")
def usage(request: Request): 
    global CONTROL_PLANE_HOST
    logger.info(f'receiving request from {request.client}')
    if CONTROL_PLANE_HOST is None:
        CONTROL_PLANE_HOST = request.client.host

    return {"status": "online"}
    


