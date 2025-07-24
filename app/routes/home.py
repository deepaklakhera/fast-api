from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def home():
    return {"message": "This is the home page"}
