from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.merchandiser import Merchandiser

router = APIRouter()

@router.get("/merchandisers")
async def listar_merchandisers(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Merchandiser))
    merchandisers = result.scalars().all()

    return [
        {
            "id": str(m.id),
            "name": m.name,
            "supervisor_id": str(m.supervisor_id) if m.supervisor_id else None
        }
        for m in merchandisers
    ]