from fastapi import APIRouter
from core.ai_model import yolo_model

router = APIRouter()

@router.get("/test-model")
async def test_model():
    if yolo_model:
        return {"status": "success", "info": "Model is ready"}
    return {"status": "error", "message": "Model not found"}