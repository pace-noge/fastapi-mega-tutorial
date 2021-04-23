from fastapi import APIRouter

router = APIRouter()


@router.get("/", tags=["main"])
def home_page():
    return {"message": "welcome"}