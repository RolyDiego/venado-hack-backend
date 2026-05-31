from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from typing import List, Tuple
from app.models.customer import Customer
from app.schemas.route_schema import (
    RouteOptimizationResponse,
    RouteStop,
    GoogleMapsWaypoint,
    GoogleMapsRouteData,
    RouteOptimizationFullResponse
)
from app.services.utils import build_distance_matrix

class RouteOptimizerService:
    @staticmethod
    def optimize_route(
        origin_lat: float, 
        origin_lon: float, 
        customers: List[Customer],
        customer_data_map: dict = None
    ) -> RouteOptimizationFullResponse:
        
        # 1. Crear lista de ubicaciones: [Origen, Cliente 1, Cliente 2, ...]
        locations: List[Tuple[float, float]] = [(origin_lat, origin_lon)]
        for c in customers:
            locations.append((float(c.latitude), float(c.longitude)))
            
        # 2. Construir la matriz de distancias
        distance_matrix = build_distance_matrix(locations)
        num_locations = len(locations)
        
        # Para hacer la ruta abierta (no necesita volver al origen),
        # agregamos un nodo dummy con distancia 0 hacia y desde todos los nodos.
        dummy_node = num_locations
        for row in distance_matrix:
            row.append(0)
        
        # Agregar la fila del nodo dummy
        distance_matrix.append([0] * (num_locations + 1))
        
        # 3. Configurar datos para OR-Tools
        data = {
            'distance_matrix': distance_matrix,
            'num_vehicles': 1,
            'starts': [0],          # El vehículo empieza en el origen
            'ends': [dummy_node]    # El vehículo termina en el nodo dummy
        }

        # Create the routing index manager
        manager = pywrapcp.RoutingIndexManager(
            len(data['distance_matrix']),
            data['num_vehicles'],
            data['starts'],
            data['ends']
        )

        # Create Routing Model
        routing = pywrapcp.RoutingModel(manager)

        # Create and register a transit callback
        def distance_callback(from_index, to_index):
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return data['distance_matrix'][from_node][to_node]

        transit_callback_index = routing.RegisterTransitCallback(distance_callback)

        # Define cost of each arc
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        # Setting first solution heuristic
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
        )

        # Solve the problem
        solution = routing.SolveWithParameters(search_parameters)

        if not solution:
            raise ValueError("No se pudo encontrar una ruta óptima")

        # 4. Extraer la solución
        route_stops = []
        total_distance_m = 0
        total_service_minutes = 0
        waypoints = []
        
        index = routing.Start(0)
        # Avanzar al primer cliente (saltamos el origen)
        index = solution.Value(routing.NextVar(index))
        order = 1
        
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            
            if node_index != dummy_node and node_index != 0:
                # Los clientes están en index_node - 1 porque el origen está en 0
                customer = customers[node_index - 1]
                
                # Obtener datos del cliente (tareas y categoría)
                customer_data = customer_data_map.get(customer.id, {}) if customer_data_map else {}
                tasks = customer_data.get("tasks", [])
                category = customer_data.get("category")
                category_display_name = customer_data.get("category_display_name")
                category_icon = customer_data.get("category_icon")
                
                route_stops.append(RouteStop(
                    order=order,
                    customer_id=customer.id,
                    code=customer.code,
                    customer_name=customer.customer_name,
                    latitude=float(customer.latitude),
                    longitude=float(customer.longitude),
                    visit_duration_minutes=customer.visit_duration_minutes,
                    category=category,
                    category_display_name=category_display_name,
                    category_icon=category_icon,
                    tasks=tasks
                ))
                
                waypoints.append(GoogleMapsWaypoint(
                    lat=float(customer.latitude),
                    lng=float(customer.longitude)
                ))
                
                total_service_minutes += customer.visit_duration_minutes
                order += 1
            
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            total_distance_m += routing.GetArcCostForVehicle(previous_index, index, 0)

        # Preparar la respuesta
        optimization_response = RouteOptimizationResponse(
            total_stops=len(route_stops),
            total_distance_km=round(total_distance_m / 1000.0, 2),
            estimated_service_minutes=total_service_minutes,
            route=route_stops
        )
        
        google_maps_data = GoogleMapsRouteData(
            origin=GoogleMapsWaypoint(lat=origin_lat, lng=origin_lon),
            waypoints=waypoints
        )
        
        return RouteOptimizationFullResponse(
            optimization=optimization_response,
            google_maps_data=google_maps_data
        )
