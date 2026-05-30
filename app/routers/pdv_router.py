from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.pdv import PDV

router = APIRouter()

@router.get("/pdvs")
def listar_pdvs(db: Session = Depends(get_db)):
    pdvs = db.query(PDV).all()
    return pdvs