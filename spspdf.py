import streamlit as st
import googlemaps
from datetime import datetime
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

# Configuração do Google Maps API
gmaps = googlemaps.Client(key='AIzaSyDp47NXg2DGMv5iZXyzNuR4JqH7VmAQbyQ')  # Substitua YOUR_API_KEY pela sua chave da API

import streamlit as st
import googlemaps
import folium
from streamlit_folium import folium_static
from datetime import datetime

def get_distance_and_duration(origin, destination):
    """Calcula distância e duração do trajeto entre dois locais."""
    result = gmaps.distance_matrix(origin, destination, mode="driving")
    if result['status'] == 'OK':
        element = result['rows'][0]['elements'][0]
        if element['status'] == 'OK':
            distance = element['distance']['text']
            duration = element['duration']['text']
            return distance, duration, element
        else:
            return "Não foi possível calcular", "Não foi possível calcular", None
    return "Erro na API", "Erro na API", None

def show_map(origin, destination, element):
    """Mostra um mapa com a localização dos endereços."""
    map = folium.Map(location=[element['distance']['value'], element['duration']['value']], zoom_start=6)
    folium.Marker(location=[element['distance']['value'], element['duration']['value']], popup='Origem').add_to(map)
    folium.Marker(location=[element['distance']['value'], element['duration']['value']], popup='Destino').add_to(map)
    folium_static(map)

# Interface do usuário no Streamlit
st.title('Calculadora de Distância')

origin = st.text_input("Endereço de Origem:", "Digite o endereço de origem aqui...")
destination = st.text_input("Endereço de Destino:", "Digite o endereço de destino aqui...")

if origin and destination:
    distance, duration, element = get_distance_and_duration(origin, destination)
    if element:
        st.success(f"A distância entre os locais é: {distance}")
        st.info(f"Tempo estimado de viagem de carro: {duration}")
        show_map(origin, destination, element)
    else:
        st.error("Não foi possível obter informações para os endereços fornecidos.")
