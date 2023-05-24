import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import folium_static

# Exemple de dataframe avec des données en France
data = pd.DataFrame({
    'Ville': ['Paris', 'Marseille', 'Lyon', 'Toulouse', 'Nice', 'Bordeaux', 'Lille'],
    'Latitude': [48.8567, 43.2964, 45.76, 43.6045, 43.7031, 44.8378, 50.6292],
    'Longitude': [2.3522, 5.3699, 4.84, 1.444, 7.2661, -0.5792, 3.0573],
    'Note': [3, 4, 2, 5, 3, 4, 5]
})

# Titre de l'application
st.title('Google Reviews en France')

# Affichage du dataframe
st.subheader('Données de notation')
st.write(data)

# Répartition des notes
st.subheader('Répartition des notes')
st.bar_chart(data['Note'].value_counts())

# Création de la carte centrée sur la France
m = folium.Map(location=[46.603354, 1.888334], zoom_start=6)

# Ajout des marqueurs pour chaque ville
for index, row in data.iterrows():
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=row['Ville'] + ': ' + str(row['Note']),
        icon=folium.Icon(color='blue')
    ).add_to(m)

# Affichage de la carte
st.subheader('Note moyenne par ville')
folium_static(m)
