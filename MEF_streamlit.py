#mise en forme de la donnée pour streamlit

import pandas as pd

# Charger le fichier CSV
locations = pd.read_csv('/content/location.csv')

# Nom de la colonne à convertir en majuscules
nom_colonne = 'city'

# Convertir le contenu de la colonne en majuscules avec prise en compte des accents
locations[nom_colonne] = locations[nom_colonne].str.normalize('NFKD') \
                                               .str.encode('ascii', errors='ignore') \
                                               .str.decode('utf-8') \
                                               .str.upper()

autres_informations = pd.read_excel('/content/gendarmerie_nationale.xlsx')
locations = locations.rename(columns={'city': 'Ville'})
resultat = pd.merge(autres_informations, locations, on='Ville', how='left')
resultat.to_csv('./coordonne_GendarN', index=False)
commentaires = pd.read_csv('/content/commentaires.csv')
commentaires = commentaires.rename(columns={'Adresse': 'Adresse_complète'})
colonnes = ['Adresse_complète','lat','lng','Ville']
coord = resultat[colonnes]
comentairesF = pd.merge(commentaires,coord,on='Adresse_complète',how='left')
comentairesF.to_csv('./commentairesF.csv', index=False)