from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.customer import Customer
from app.models.market import Market
from app.models.merchandiser import Merchandiser
from app.models.supervisor import Supervisor

router = APIRouter()

@router.get("/customers")
def listar_customers(db: Session = Depends(get_db)):
    data = (
        db.query(Customer, Market, Merchandiser, Supervisor)
        .join(Market, Customer.market_id == Market.id)
        .outerjoin(Merchandiser, Customer.merchandiser_id == Merchandiser.id)
        .outerjoin(Supervisor, Merchandiser.supervisor_id == Supervisor.id)
        .all()
    )

    return [
        {
            "id": str(customer.id),
            "code": customer.code,
            "customer_name": customer.customer_name,
            "category": customer.category,
            "market": market.name if market else None,
            "latitude": float(customer.latitude) if customer.latitude is not None else None,
            "longitude": float(customer.longitude) if customer.longitude is not None else None,
            "visit_duration_minutes": customer.visit_duration_minutes,
            "merchandiser": merchandiser.name if merchandiser else None,
            "supervisor": supervisor.name if supervisor else None,
        }
        for customer, market, merchandiser, supervisor in data
    ]


@router.get("/customers/map")
def customers_para_mapa(db: Session = Depends(get_db)):
    customers = db.query(Customer).all()

    return [
        {
            "id": str(c.id),
            "code": c.code,
            "name": c.customer_name,
            "category": c.category,
            "lat": float(c.latitude) if c.latitude is not None else None,
            "lng": float(c.longitude) if c.longitude is not None else None,
            "duration": c.visit_duration_minutes,
        }
        for c in customers
    ]