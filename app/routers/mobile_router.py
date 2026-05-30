from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db
from app.models.customer import Customer
from app.models.customer_visit_day import CustomerVisitDay
from app.models.merchandiser import Merchandiser
from app.models.market import Market

router = APIRouter()

@router.get("/ruta-dia/{merchandiser_id}")
def obtener_ruta_dia(merchandiser_id: str, db: Session = Depends(get_db)):
    # Python: lunes=0, martes=1, ..., domingo=6
    dia_actual = datetime.now().weekday()

    merchandiser = db.query(Merchandiser).filter(
        Merchandiser.id == merchandiser_id
    ).first()

    if not merchandiser:
        return {"error": "Reponedor no encontrado"}

    data = (
        db.query(Customer, Market)
        .join(CustomerVisitDay, CustomerVisitDay.customer_id == Customer.id)
        .join(Market, Customer.market_id == Market.id)
        .filter(Customer.merchandiser_id == merchandiser_id)
        .filter(CustomerVisitDay.day_of_week == dia_actual)
        .all()
    )

    return {
        "merchandiser": {
            "id": str(merchandiser.id),
            "name": merchandiser.name
        },
        "day_of_week": dia_actual,
        "total_customers": len(data),
        "customers": [
            {
                "id": str(customer.id),
                "code": customer.code,
                "name": customer.customer_name,
                "category": customer.category,
                "market": market.name,
                "latitude": float(customer.latitude),
                "longitude": float(customer.longitude),
                "visit_duration_minutes": customer.visit_duration_minutes
            }
            for customer, market in data
        ]
    }