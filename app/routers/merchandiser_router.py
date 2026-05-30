from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.merchandiser import Merchandiser

router = APIRouter()

@router.get("/merchandisers")
def listar_merchandisers(db: Session = Depends(get_db)):

    merchandisers = db.query(Merchandiser).all()

    return [
        {
            "id": str(m.id),
            "name": m.name,
            "supervisor_id": str(m.supervisor_id) if m.supervisor_id else None
        }
        for m in merchandisers
    ]