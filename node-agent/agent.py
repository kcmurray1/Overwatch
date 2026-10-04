import psutil
import os
import threading
import docker
import requests
import socket
from routers import DockerRouter, SystemRouter, AgentRouter
from routers.system import UsageMonitor

CONTROL_PLANE_HOST = None


def watch_docker_events():
    global CONTROL_PLANE_HOST
    try:
        client = docker.from_env()  # Automatically picks up unix://var/run/docker.sock
        print("Started watching local Docker events...")
        
       
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
                print('event triggered')
            except Exception as e:
                print("container get error", str(e))
            
            # send request to control plane host
            if CONTROL_PLANE_HOST:
                try:
                    print(payload)
                    print('sending host udpated!')
                    requests.post(f"http://{CONTROL_PLANE_HOST}:5000/containers/event", json=payload, timeout=3)
                except Exception as e:
                    print(f"error sending event {e}")
                
    except Exception as e:
        print(f"Docker event listener crashed: {e}")

def write_pid():
    pid = os.getpid()
    with open("agent.pid", "w") as f:
        f.write(str(pid))

from fastapi import FastAPI, Request
from contextlib import asynccontextmanager

# https://fastapi.tiangolo.com/advanced/events/#lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    write_pid()
    threading.Thread(target=watch_docker_events, daemon=True).start()
    UsageMonitor.start_background_monitor()
    yield



app = FastAPI(lifespan=lifespan)

app.include_router(SystemRouter)
app.include_router(AgentRouter)
app.include_router(DockerRouter)

@app.get("/")
def usage(request: Request): 
    global CONTROL_PLANE_HOST
    print(request.client)
    if CONTROL_PLANE_HOST is None:
        print('updated host')
        CONTROL_PLANE_HOST = request.client.host

    return {"status": "online"}
    


