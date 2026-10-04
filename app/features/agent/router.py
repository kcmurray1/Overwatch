from fastapi import APIRouter, HTTPException
import httpx
from app.core.responses import response_template

router = APIRouter(
    prefix="/agents",
    tags=["agents"]
)


@router.get("/update")
async def update_agent():
    
    TEST_URL = "100.95.32.59"
    try:
        async with httpx.AsyncClient(base_url="http://127.0.0.1:8001") as client:
            res = await client.post("/watchdog/reload", json=payload)
            res.raise_for_status()
            
        return {"status": "accepted", "message": "Update handed off to local watchdog."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to communicate with Watchdog: {str(e)}")
    
