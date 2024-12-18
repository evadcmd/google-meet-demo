from fastapi import APIRouter

router = APIRouter(prefix="/healthz", tags=["liveness prove"])


@router.get(path="", status_code=200)
async def liveness():
    return
