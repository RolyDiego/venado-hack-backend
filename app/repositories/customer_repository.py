from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from typing import List, Optional

from app.models.customer import Customer, CustomerVisitDay


class CustomerRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_customers_by_merchandiser_and_day(
        self, 
        merchandiser_id: UUID, 
        day_of_week: int
    ) -> List[Customer]:
        """
        Get all customers assigned to a merchandiser that should be visited on a specific day.
        
        Args:
            merchandiser_id: UUID of the merchandiser
            day_of_week: Day of week (1=Monday, 6=Saturday)
            
        Returns:
            List of Customer objects
        """
        query = (
            select(Customer)
            .join(CustomerVisitDay, Customer.id == CustomerVisitDay.customer_id)
            .where(
                Customer.merchandiser_id == merchandiser_id,
                CustomerVisitDay.day_of_week == day_of_week
            )
            .order_by(Customer.code)
        )
        
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_customer_by_id(self, customer_id: UUID) -> Optional[Customer]:
        """
        Get a customer by ID.
        
        Args:
            customer_id: UUID of the customer
            
        Returns:
            Customer object or None
        """
        query = select(Customer).where(Customer.id == customer_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
