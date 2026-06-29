from fastapi import APIRouter, UploadFile, File
from services.detector_service import detect_fields

router = APIRouter(
    prefix="/detect",
    tags=["Detection"]
)


@router.post("/")
async def detect(file: UploadFile = File(...)):
    return detect_fields(file)