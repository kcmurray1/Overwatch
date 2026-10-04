from fastapi import FastAPI, Request
from sqlmodel import SQLModel, Session
from contextlib import asynccontextmanager
import os
import asyncio
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings
from app.features.machines.manager import MachineManager
from .dependencies import engine, get_session
from .features.containers import router as container_router
from .features.machines import router as machine_router
from app.core.exceptions import AppBaseException
from app.core.responses import response_template

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

@app.exception_handler(AppBaseException)
async def homelab_exception_handler(request: Request, exc: AppBaseException):
    return response_template(
        status=exc.status_code,
        message=exc.message,
        data=exc.data
    )

app.include_router(machine_router.router)
app.include_router(container_router.router)
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