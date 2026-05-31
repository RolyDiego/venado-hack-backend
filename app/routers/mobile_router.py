from fastapi import APIRouter, Depends
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.customer import Customer
from app.models.customer_visit_day import CustomerVisitDay
from app.models.merchandiser import Merchandiser
from app.models.market import Market

router = APIRouter()


@router.get("/ruta-dia/{merchandiser_id}")
async def obtener_ruta_dia(
    merchandiser_id: str,
    db: AsyncSession = Depends(get_db)
):
    dia_actual = datetime.now().weekday() -2

    result = await db.execute(
        select(Merchandiser).where(
            Merchandiser.id == merchandiser_id
        )
    )

    merchandiser = result.scalar_one_or_none()

    if not merchandiser:
        return {"error": "Reponedor no encontrado"}

    result = await db.execute(
        select(Customer, Market)
        .join(CustomerVisitDay, CustomerVisitDay.customer_id == Customer.id)
        .join(Market, Customer.market_id == Market.id)
        .where(Customer.merchandiser_id == merchandiser_id)
        .where(CustomerVisitDay.day_of_week == dia_actual)
    )

    data = result.all()

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