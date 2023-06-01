import streamlit as st
import pandas as pd
import folium
import plotly.express as px
import matplotlib.pyplot as plt
from wordcloud import WordCloud
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
    
    # Supprimer les lignes avec des valeurs NaN dans les colonnes 'lat' et 'lng'
    data = data.dropna(subset=['lat', 'lng'])
    
    # Option pour afficher les commentaires vides ou non
    show_empty_comments = st.checkbox("Afficher les commentaires vides")
    
    # Répartition des notes
    st.subheader('Répartition des notes')
    
    # Filtrer les données pour exclure les commentaires vides si l'option est désactivée
    if not show_empty_comments:
        data = data.dropna(subset=['Commentaire_x'])
    
    # Créer le graphe de répartition des notes
    st.bar_chart(data['Note_x'].value_counts())
    
    # Calculer la moyenne des notes par ville
    average_ratings = data.groupby('Ville')['Note_x'].mean().reset_index()
    sorted_cities = data['Ville'].sort_values().unique()
    
    # Création de la carte centrée sur la France
    m = folium.Map(location=[46.603354, 1.888334], zoom_start=6)
    
    # Ajout des marqueurs pour chaque ville avec la moyenne des notes dans le pop-up
    for index, row in data.iterrows():
        ville = row['Ville']
        lat = row['lat']
        lng = row['lng']
        note = average_ratings.loc[average_ratings['Ville'] == ville, 'Note_x'].values[0]
        
        if note < 2 and note < 3:
            color = 'red'
        elif note >= 3.00 and note < 4:
            color = 'orange'
        elif note >= 4.00 and note <= 5.00:
            color = 'green'
        
        folium.Marker(
            location=[lat, lng],
            popup=f"{ville}: {note:.2f}",
            icon=folium.Icon(color=color)
        ).add_to(m)
    
    # Affichage de la carte
    st.subheader('Note moyenne par ville')
    folium_static(m)
    
    selected_city = st.selectbox('Sélectionnez une ville', sorted_cities)
    
    # Groupement des données par ville et extraction des dates uniques pour chaque ville
    dates_by_city = data.groupby('Ville')['Date_x'].unique()
    
    # Sélection de la date
    selected_date = st.selectbox('Sélectionnez une date', dates_by_city[selected_city])
    
    # Filtrer les données en fonction de la ville et de la date sélectionnées
    filtered_data = data[(data['Ville'] == selected_city) & (data['Date_x'] == selected_date)]
    
    # Filtrer les commentaires vides pour la ville sélectionnée si l'option est désactivée
    if not show_empty_comments:
        filtered_data = filtered_data.dropna(subset=['Commentaire_x'])
    
    # Vérifier s'il y a des commentaires à afficher
    if not filtered_data.empty:
        st.subheader(f"Commentaires pour {selected_city} {selected_date}")
        st.write(filtered_data['Commentaire_x'])
    else:
        st.subheader(f"Aucun commentaire disponible pour {selected_city} {selected_date}")
    
    # Répartition des sujets
    st.subheader('Répartition des sujets')
    subject_counts = data['subject_name'].value_counts()
    
    fig = px.pie(subject_counts, values=subject_counts.values, names=subject_counts.index)
    st.plotly_chart(fig)
    
    # Générer le nuage de mots pour les avis négatifs
    negative_reviews = data[data['Note_x'] =< 3]
    negative_wordcloud = WordCloud().generate(' '.join(negative_reviews['desc_clean'].dropna()))

    
    # Afficher le nuage de mots des termes les plus fréquents dans les avis négatifs
    st.subheader("Nuage de mots des termes les plus fréquents dans les avis négatifs")
    plt.imshow(negative_wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot()
