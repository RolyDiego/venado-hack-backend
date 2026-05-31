from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.merchandiser import Merchandiser
from app.models.supervisor import Supervisor

router = APIRouter(prefix="/auth", tags=["Auth"])

class LoginRequest(BaseModel):
    username: str
    password: str
    canal: str  # "app" o "web"

@router.post("/login")
async def login(data: LoginRequest, db: AsyncSession = Depends(get_db)):

    if data.password != "123":
        raise HTTPException(status_code=401, detail="Password incorrecto")

    canal = data.canal.lower().strip()
    username = data.username.strip()

    if canal == "app":
        result = await db.execute(
            select(Merchandiser).where(Merchandiser.name == username)
        )
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=404, detail="Reponedor no encontrado")

        return {
            "success": True,
            "role": "merchandiser",
            "canal": "app",
            "user": {
                "id": str(user.id),
                "name": user.name,
                "supervisor_id": str(user.supervisor_id) if user.supervisor_id else None
            }
        }

    if canal == "web":
        result = await db.execute(
            select(Supervisor).where(Supervisor.name == username)
        )
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=404, detail="Supervisor no encontrado")

        return {
            "success": True,
            "role": "supervisor",
            "canal": "web",
            "user": {
                "id": str(user.id),
                "name": user.name
            }
        }

    raise HTTPException(status_code=400, detail="Canal inválido. Use 'app' o 'web'")