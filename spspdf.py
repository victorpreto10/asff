import streamlit as st
import googlemaps
from datetime import datetime
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

# Configuração do Google Maps API
gmaps = googlemaps.Client(key='AIzaSyDp47NXg2DGMv5iZXyzNuR4JqH7VmAQbyQ')  # Substitua YOUR_API_KEY pela sua chave da API


def get_distance_and_duration(origin, destination):
    """Calcula distância e duração do trajeto entre dois locais."""
    result = gmaps.distance_matrix(origin, destination, mode="driving")
    if result['status'] == 'OK':
        element = result['rows'][0]['elements'][0]
        if element['status'] == 'OK':
            distance = element['distance']['text']
            duration = element['duration']['text']
            return distance, duration
        else:
            return "Não foi possível calcular", "Não foi possível calcular"
    return "Erro na API", "Erro na API"

# Interface do usuário no Streamlit
st.title('Calculadora de Distância')

origin = st.text_input("Endereço de Origem:", "Digite o endereço de origem aqui...")
destination = st.text_input("Endereço de Destino:", "Digite o endereço de destino aqui...")

if st.button('Calcular Distância'):
    if origin and destination:
        distance, duration = get_distance_and_duration(origin, destination)
        st.success(f"A distância entre os locais é: {distance}")
        st.info(f"Tempo estimado de viagem de carro: {duration}")
    else:
        st.error("Por favor, insira ambos os endereços para calcular a distância.")
