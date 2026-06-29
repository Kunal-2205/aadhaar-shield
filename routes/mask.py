from fastapi import APIRouter
from fastapi.responses import FileResponse
from pydantic import BaseModel

from services.mask_service import mask_fields

router = APIRouter(
    prefix="/mask",
    tags=["Mask"]
)


class MaskRequest(BaseModel):

    image_id: str

    selected_ids: list[int]

    mask_type: str = "black"


@router.post("/")
def mask(request: MaskRequest):

    output = mask_fields(
        image_id=request.image_id,
        selected_ids=request.selected_ids,
        mask_type=request.mask_type
    )

    return FileResponse(
        path=output,
        media_type="image/jpeg",
        filename="masked.jpg"
    )