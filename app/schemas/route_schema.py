from pydantic import BaseModel, Field
from uuid import UUID
from typing import List, Optional


class RouteOptimizationRequest(BaseModel):
    merchandiser_id: UUID
    latitude: float = Field(..., ge=-90, le=90, description="Current latitude of merchandiser")
    longitude: float = Field(..., ge=-180, le=180, description="Current longitude of merchandiser")
    day_of_week: int = Field(..., ge=1, le=6, description="Day of week (1=Monday, 6=Saturday)")


class CustomerData(BaseModel):
    id: UUID
    code: str
    customer_name: str
    latitude: float
    longitude: float
    visit_duration_minutes: int


class RouteStop(BaseModel):
    order: int
    customer_id: UUID
    code: str
    customer_name: str
    latitude: float
    longitude: float
    visit_duration_minutes: int


class RouteOptimizationResponse(BaseModel):
    total_stops: int
    total_distance_km: float
    estimated_service_minutes: int
    route: List[RouteStop]


class GoogleMapsWaypoint(BaseModel):
    lat: float
    lng: float


class GoogleMapsRouteData(BaseModel):
    origin: GoogleMapsWaypoint
    waypoints: List[GoogleMapsWaypoint]


class RouteOptimizationFullResponse(BaseModel):
    optimization: RouteOptimizationResponse
    google_maps_data: GoogleMapsRouteData
