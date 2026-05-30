from fastapi import APIRouter

router = APIRouter(prefix="/mobile", tags=["mobile"])

@router.get("")
async def get_mobile_root():
    return {"message": "Mobile API root"}
