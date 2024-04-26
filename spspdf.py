import streamlit as st
import googlemaps
from datetime import datetime
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

# Configuração do Google Maps API
gmaps = googlemaps.Client(key='AIzaSyDp47NXg2DGMv5iZXyzNuR4JqH7VmAQbyQ')  # Substitua YOUR_API_KEY pela sua chave da API

def get_distance_matrix(addresses):
    matrix = gmaps.distance_matrix(addresses, addresses, mode="driving")
    distances = []
    for row in matrix['rows']:
        row_distances = []
        for element in row['elements']:
            if element['status'] == 'OK':  # Verifica se o status do elemento é OK
                row_distances.append(element['duration']['value'])
            else:
                row_distances.append(None)  # Pode usar None ou um valor padrão se a API retornar um erro
        distances.append(row_distances)
    return distances


def compute_routes(distance_matrix, num_vehicles):
    """Calcula rotas otimizadas usando o OR-Tools."""
    manager = pywrapcp.RoutingIndexManager(len(distance_matrix), num_vehicles, 0)
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return distance_matrix[from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC

    solution = routing.SolveWithParameters(search_parameters)
    if not solution:
        return []

    routes = []
    for vehicle_id in range(num_vehicles):
        index = routing.Start(vehicle_id)
        route = []
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            route.append(node_index)
            index = solution.Value(routing.NextVar(index))
        routes.append(route)
    return routes

# Streamlit app
st.title("Dashboard de Otimização de Rotas")

# User input for addresses
addresses = st.text_area("Insira os endereços:", height=300, help="Digite cada endereço em uma nova linha.")
num_vehicles = st.number_input("Número de Motoristas:", min_value=1, max_value=10, value=1)

if st.button("Calcular Rotas"):
    if addresses:
        address_list = addresses.split('\n')
        distance_matrix = get_distance_matrix(address_list)
        routes = compute_routes(distance_matrix, num_vehicles)

        # Exibir rotas
        for i, route in enumerate(routes):
            st.subheader(f"Rota para Motorista {i+1}")
            route_addresses = [address_list[idx] for idx in route]
            st.write(" -> ".join(route_addresses))
