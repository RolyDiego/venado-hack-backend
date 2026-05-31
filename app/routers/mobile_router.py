from fastapi import APIRouter, Depends
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.customer import Customer
from app.models.customer_visit_day import CustomerVisitDay
from app.models.merchandiser import Merchandiser
from app.models.market import Market
from app.models.market_category import MarketCategory, CategoryTask
from app.schemas.route_schema import CategoryTasksResponse

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
        select(Customer, Market, MarketCategory)
        .join(CustomerVisitDay, CustomerVisitDay.customer_id == Customer.id)
        .join(Market, Customer.market_id == Market.id)
        .outerjoin(MarketCategory, Market.category_id == MarketCategory.id)
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
                "visit_duration_minutes": customer.visit_duration_minutes,
                "category_display_name": category.display_name if category else None,
                "category_icon": category.icon_name if category else None
            }
            for customer, market, category in data
        ]
    }


@router.get("/tareas-categoria/{category_id}", response_model=CategoryTasksResponse)
async def obtener_tareas_categoria(
    category_id: str,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(CategoryTask).where(CategoryTask.category_id == category_id)
    )
    tasks = result.scalars().all()

    return CategoryTasksResponse(
        category_id=category_id,
        total_tasks=len(tasks),
        total_estimated_time_mins=sum(task.estimated_time_mins for task in tasks),
        tasks=[
            {
                "id": task.id,
                "task_description": task.task_description,
                "estimated_time_mins": task.estimated_time_mins
            }
            for task in tasks
        ]
    )


@router.get("/tareas-empresa/{customer_id}", response_model=CategoryTasksResponse)
async def obtener_tareas_empresa(
    customer_id: str,
    db: AsyncSession = Depends(get_db)
):
    # First get the customer's market
    result = await db.execute(
        select(Customer).where(Customer.id == customer_id)
    )
    customer = result.scalar_one_or_none()

    if not customer:
        return {"error": "Cliente no encontrado"}

    # Get the market's category_id
    result = await db.execute(
        select(Market).where(Market.id == customer.market_id)
    )
    market = result.scalar_one_or_none()

    if not market:
        return {"error": "Empresa no encontrada"}

    if not market.category_id:
        return {"error": "La empresa no tiene categoría asignada"}

    # Get tasks for the category
    result = await db.execute(
        select(CategoryTask).where(CategoryTask.category_id == market.category_id)
    )
    tasks = result.scalars().all()

    return CategoryTasksResponse(
        category_id=str(market.category_id),
        total_tasks=len(tasks),
        total_estimated_time_mins=sum(task.estimated_time_mins for task in tasks),
        tasks=[
            {
                "id": task.id,
                "task_description": task.task_description,
                "estimated_time_mins": task.estimated_time_mins
            }
            for task in tasks
        ]
    )