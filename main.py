from fastapi import FastAPI

from routes.detect import router as detect_router
from routes.mask import router as mask_router

app = FastAPI(
    title="Aadhaar Masking API",
    version="1.0"
)

# Register routers
app.include_router(detect_router)
app.include_router(mask_router)


@app.get("/")
def home():
    return {
        "message": "Aadhaar Masking API Running"
    }