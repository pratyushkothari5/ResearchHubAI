from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def list_papers():
    return {"papers": []}
