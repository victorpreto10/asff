import streamlit as st
from streamlit_folium import folium_static
import folium

# Título da aplicação
st.title('Interactive Map Viewer')

# Entradas do usuário para latitude e longitude
latitude = st.number_input('Enter latitude:', value=40.1215, format="%.4f")
longitude = st.number_input('Enter longitude:', value=-100.4504, format="%.4f")

# Criar um mapa centrado nas coordenadas inseridas
map = folium.Map(location=[latitude, longitude], zoom_start=4)

# Adicionar um marcador ao mapa
folium.Marker([latitude, longitude], popup='Your location', tooltip='Click me!').add_to(map)

# Mostrar o mapa na aplicação Streamlit
folium_static(map)
