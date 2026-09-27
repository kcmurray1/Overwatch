from fastapi import FastAPI
from sqlmodel import SQLModel, Session
from .routers import machine, project, blueprint, docker
from contextlib import asynccontextmanager
from .dependencies import engine, get_session
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings
from app.machine_manager import MachineManager
import os
import asyncio

        
async def check_connections_v2():
    while True:
        try:
            # Use engine context directly for background tasks
            with Session(engine) as session:
                await MachineManager.check_agent_connections(session)
        except Exception as e:
            print(f"Error in check_connections background loop: {e}")

        await asyncio.sleep(15)

@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    key_path = settings.key_path
    
    ssh_config_path = "/root/.ssh/config"
    os.makedirs("/root/.ssh", exist_ok=True)
    
    with open(ssh_config_path, "w") as f:
        f.write(f"""
            Host *
                IdentityFile {key_path}
                StrictHostKeyChecking no
                UserKnownHostsFile /dev/null
                IdentitiesOnly yes
        """)
    os.chmod(ssh_config_path, 0o600)

    bg_task = asyncio.create_task(check_connections_v2())
    
    yield
    bg_task.cancel()
    print("Shutting down control plane...")


app = FastAPI(lifespan=lifespan)

app.include_router(machine.router)
app.include_router(project.router)
app.include_router(blueprint.router)
app.include_router(docker.router)
SQLModel.metadata.create_all(engine)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:4173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "App is Running!"}