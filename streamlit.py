import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import folium_static

# Titre de l'application
st.title('Google Reviews en France')

# Téléchargement du fichier
uploaded_file = st.file_uploader("Télécharger le fichier CSV", type="csv")

# Vérification si un fichier a été téléchargé
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file, encoding='utf-8')
    
    # Affichage du dataframe
    st.subheader('Données de notation')
    st.write(data)
    
    # Répartition des notes
    st.subheader('Répartition des notes')
    st.bar_chart(data['Note'].value_counts())
    
    # Supprimer les lignes avec des valeurs NaN dans les colonnes 'lat' et 'lng' parce que sinon planté
    data = data.dropna(subset=['lat', 'lng'])
    
    # Calculer la moyenne des notes par ville
    average_ratings = data.groupby('Ville')['Note'].mean().reset_index()
    sorted_cities = data['Ville'].sort_values().unique()
    
    # Création de la carte centrée sur la France
    m = folium.Map(location=[46.603354, 1.888334], zoom_start=6)
    
    # Ajout des marqueurs pour chaque ville avec la moyenne des notes dans le pop-up
    for index, row in data.iterrows():
        ville = row['Ville']
        lat = row['lat']
        lng = row['lng']
        note = average_ratings.loc[average_ratings['Ville'] == ville, 'Note'].values[0]
        
        folium.Marker(
            location=[lat, lng],
            popup=f"{ville}: {note:.2f}",
            icon=folium.Icon(color='blue')
        ).add_to(m)
    
    # Affichage de la carte
    st.subheader('Note moyenne par ville')
    folium_static(m)
    
    selected_city = st.selectbox('Sélectionnez une ville', sorted_cities)

    sorted_date = data['Date'].sort_values().unique()
    selected_date = st.selectbox('Sélectionnez une date', sorted_date)

    filtered_data = data[data['Date'] == selected_date]

    
    # Filtrer les commentaires vides pour la ville sélectionnée
    selected_comments = filtered_data[filtered_data['Ville'] == selected_city]['Commentaire'].dropna()

    
    # Vérifier s'il y a des commentaires à afficher
    if not selected_comments.empty:
        st.subheader(f"Commentaires pour {selected_city}")
        st.write(selected_comments)
    else:
        st.subheader(f"Aucun commentaire disponible pour {selected_city}")
