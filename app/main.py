from fastapi import FastAPI
from sqlmodel import SQLModel
from .routers import machine
from contextlib import asynccontextmanager
from .dependencies import engine, get_session
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings
from app.machine_manager import MachineManager
import os
import asyncio

async def check_connections():
    while True:
        # 1. Create the generator object
        session_generator = get_session()
        session = None
        try:
            # 2. Advance the generator to the 'yield' statement to get the session
            session = next(session_generator)
            
            # 3. Run your task
            await MachineManager.check_connections(session, get_settings().key_path)
            
        except Exception as e:
            print(f"❌ Error in check_connections background loop: {e}")
        finally:
            # 4. Clean up the generator by advancing it past the yield (executes finally blocks)
            if session is not None:
                try:
                    next(session_generator)
                except StopIteration:
                    pass  # StopIteration is normal when a generator finishes
        
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

    bg_task = asyncio.create_task(check_connections())
    
    yield
    bg_task.cancel()
    print("Shutting down control plane...")


app = FastAPI(lifespan=lifespan)

app.include_router(machine.router)
# app.include_router(edge.router)
# app.include_router(task.router)
# app.include_router(project.router)
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