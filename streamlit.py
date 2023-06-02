import streamlit as st
import pandas as pd
import folium
import plotly.express as px
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from streamlit_folium import folium_static
import plotly.graph_objects as go
import dateparser

# Titre de l'application
st.title('Google Reviews en France')

# Téléchargement du fichier
uploaded_file = st.file_uploader("Télécharger le fichier CSV", type="csv")

# Vérification si un fichier a été téléchargé
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file, encoding='utf-8')
    
    # Nombre de commentaires différents
    num_unique_comments = data['Commentaire_x'].nunique()
    st.subheader(f"Nombre de commentaires différents : {num_unique_comments}")
    
    # Note moyenne globale
    average_rating = data['Note_x'].mean()
    st.subheader(f"Note moyenne globale : {average_rating:.2f}")
    
    # Pourcentage de commentaires non vides par rapport au total
    non_empty_comments_percentage = (data['Commentaire_x'].notna().sum() / len(data)) * 100
    st.subheader(f"Pourcentage de commentaires non vides : {non_empty_comments_percentage:.2f}%")
        
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
    
    # Créer le graphe de répartition des notes en fonction de la période
    st.subheader("Répartition des notes en fonction de la période")
    
    # Ajoutez la fonction de conversion des expressions de date en objets de date Python
    def parse_date(date_string):
        parsed_date = dateparser.parse(date_string)
        return parsed_date.date()

    # Convertissez les expressions de date en objets de date
    data['Date_maj'] = data['Date_x'].apply(parse_date)

    # Sélection de la période
    start_date = st.date_input("Date de début", value=pd.to_datetime("2022-06-02").date())
    end_date = st.date_input("Date de fin")

    # Filtrez les données en fonction de la période sélectionnée
    filtered_data = data[(data['Date_maj'] >= start_date) & (data['Date_maj'] <= end_date)]

    # Créer le graphe de répartition des notes en fonction de la période
    fig = go.Figure(data=[go.Bar(x=filtered_data['Date_maj'].value_counts().index,
                                y=filtered_data['Date_maj'].value_counts().values)])

    fig.update_layout(title="Nombre de notes en fonction de la période",
                      xaxis_title="Période",
                      yaxis_title="Nombre de notes")

    # Affichage du graphe
    st.plotly_chart(fig)
    
    # Graphe d'évolution du nombre d'avis négatifs
    # Filtrer les avis négatifs
    negative_reviews = data[data['Note_x'] <= 3]

    # Compter le nombre d'avis négatifs par date
    negative_reviews_count = negative_reviews['Date_maj'].value_counts().sort_index()

    # Créer le graphe d'évolution du nombre d'avis négatifs
    fig_negative_reviews = go.Figure(data=go.Scatter(x=negative_reviews_count.index, y=negative_reviews_count.values))
    fig_negative_reviews.update_layout(title="Évolution du nombre d'avis négatifs",
                                       xaxis_title="Date",
                                       yaxis_title="Nombre d'avis négatifs")
    
    # Affichage du graphe d'évolution du nombre d'avis négatifs
    st.plotly_chart(fig_negative_reviews)
    
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
    
    # Ajouter la moyenne de la ville sélectionnée sans tenir compte de la date
    average_rating_selected_city = average_ratings.loc[average_ratings['Ville'] == selected_city, 'Note_x'].values[0]
    st.subheader(f"Note moyenne de {selected_city} : {average_rating_selected_city:.2f}")
    
    # Répartition des sujets
    st.subheader('Répartition des sujets')
    subject_counts = data['subject_name'].value_counts()
    
    fig = px.pie(subject_counts, values=subject_counts.values, names=subject_counts.index)
    st.plotly_chart(fig)
    
    # Générer le nuage de mots pour les avis négatifs
    negative_reviews = data[data['Note_x'] <= 3]
    negative_wordcloud = WordCloud().generate(' '.join(negative_reviews['desc_clean'].dropna()))

    # Afficher le nuage de mots des termes les plus fréquents dans les avis négatifs
    st.subheader("Nuage de mots des termes les plus fréquents dans les avis négatifs")
    plt.imshow(negative_wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot()


