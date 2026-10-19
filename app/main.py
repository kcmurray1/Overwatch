from fastapi import FastAPI, Request
from sqlmodel import SQLModel, Session
from contextlib import asynccontextmanager
import os
import asyncio
import json
from pathlib import Path
from sqlmodel import Session, select
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings
from app.features.machines.manager import MachineManager
from .dependencies import engine, get_session
from .features.containers import router as container_router
from .features.machines import router as machine_router
from .features.agent import router as agent_router
from app.core.exceptions import AppBaseException
from app.core.responses import response_template
from app.features.containers.schemas import ContainerConfig

def seed_container_configs():
    """Scans the app/configs directory and seeds any .json templates into SQLite if they don't exist."""
    # Assuming your main.py is in app/, configs/ will be right alongside it
    config_dir = Path(__file__).parent / "core/configs/containers"
    
    if not config_dir.exists():
        print(f"Configs directory not found at {config_dir}, skipping seed.")
        return

    with Session(engine) as session:
        for file_path in config_dir.glob("*.json"):
            try:
                with open(file_path, "r") as f:
                    template = json.load(f)
                
                name = template.get("name")
                if not name:
                    continue
                
                # Check if this config template name already exists in SQLite
                statement = select(ContainerConfig).where(ContainerConfig.name == name)
                existing = session.exec(statement).first()
                
                if not existing:
                    print(f"Seeding container config: {name} (from {file_path.name})")
                    new_config = ContainerConfig(
                        name=name,
                        description=template.get("description"),
                        spec=template.get("spec", {})
                    )
                    session.add(new_config)
                    
            except Exception as e:
                print(f"Failed to load seed config {file_path.name}: {e}")
                
        session.commit()

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
    
    seed_container_configs()
    
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
app.include_router(agent_router.router)
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