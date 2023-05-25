from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import pandas as pd
import time
import re

class GoogleMaps:
    def __init__(self):
        # Remplacez le chemin vers le driver de votre navigateur
        driver_path = 'chromedriver'
        service = Service(executable_path=driver_path)
        self.driver = webdriver.Chrome(service=service)
        self.search_success = False

    def search_location(self, location):
        # Ouvrir Google Maps
        self.driver.get('https://www.google.com/maps/')
        skip = self.driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/div[1]/form[1]/div/div/button/span').click()
        search_box = self.driver.find_element(By.XPATH, '//*[@id="searchboxinput"]')
        search_box.send_keys(location)
        search_box.send_keys(Keys.ENTER)
        time.sleep(10)

        try:
            # Essayer de cliquer sur le bouton
            button = self.driver.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[3]/div/div/button[2]/div[2]/div[2]')
            button.click()
            time.sleep(10)
            trier = self.driver.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[3]/div[8]/div[2]/button/span/span')
            trier.click()
            time.sleep(5)
            newest = self.driver.find_element(By.XPATH, '//*[@id="action-menu"]/div[2]')
            newest.click()
            time.sleep(5)
            self.search_success = True
        except NoSuchElementException:
            # L'élément n'a pas été trouvé, la recherche a échoué
            self.search_success = False

    def get_rating(self, review):
        star_elements = review.find_all('img', {'class': 'hCCjke vzX5Ic'})
        return len(star_elements)

    def get_reviews(self, location, reviews, output_file):
        # Attente supplémentaire pour charger les avis
        time.sleep(10)

        # Extraire la page HTML
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')

        # Extraire les avis
        review_list = soup.find_all('div', {'class': 'jftiEf fontBodyMedium'})

        # Parcourir les avis et les ajouter à la liste
        for index, review in enumerate(review_list):
            author = review.find('div', {'class': 'd4r55'}).text.strip()
            date_element = review.find('span', {'class': 'rsqaWe'})
            if date_element is not None:
                date = date_element.text.strip()
                skip_comment = False  # Variable pour indiquer si le commentaire doit être ignoré
                if 'ans' in date and not re.search(r'il y a 2\s*ans', date, re.IGNORECASE):
                    continue  # Passer au commentaire suivant si la date ne contient pas 'il y a 2 ans'
                date = re.sub(r'\s+', ' ', date)  # Supprimer les espaces supplémentaires

            else:
                date = ""

            rating = self.get_rating(review)
            comment_element = review.find('span', {'class': 'wiI7pd'})
            if comment_element is not None:
                comment = comment_element.text.strip()
                comment = clean_comment(comment)  # Appel de la fonction clean_comment
            else:
                comment = ""

            reviews.append([index + 1, location, author, date, rating, comment])  # Ajout de l'index dans la liste des avis
            print(author)

            # Écrire l'avis dans le fichier CSV au fur et à mesure
            df = pd.DataFrame(reviews, columns=['Index', 'Adresse', 'Auteur', 'Date', 'Note', 'Commentaire'])
            df.to_csv(output_file, index=False)

    def close(self):
        # Fermer le navigateur
        self.driver.quit()


def clean_comment(comment):
    # Nettoyer le commentaire en supprimant les retours à la ligne, la ponctuation, les accents, etc.
    comment = re.sub(r'\n', ' ', comment)  # Supprimer les retours à la ligne
    comment = re.sub(r'[^\w\s]', ' ', comment)  # Supprimer la ponctuation
    comment = re.sub(r'[^\x00-\x7F]+', ' ', comment)  # Supprimer les caractères non ASCII
    return comment


maps = GoogleMaps()

# Liste pour stocker les avis
reviews = []
no_match = []

# Lire le fichier Excel
GN = pd.read_excel('./gendarmerie_nationale.xlsx')

# Chemin du fichier CSV de sortie
output_file = 'commentaires.csv'
no_match_file = 'no_match.csv'

# Itérer sur chaque ligne du DataFrame
for index, row in GN.iterrows():
    # Créer une nouvelle instance de GoogleMaps pour chaque ligne
    maps = GoogleMaps()

    location = row['Adresse_complète']
    print(location)

    # Rechercher les avis pour chaque emplacement
    maps.search_location(location)

    # Vérifier si la recherche a réussi ou non
    if not maps.search_success:
        print("La recherche n'a pas abouti pour l'adresse:", location)
        no_match.append(["La recherche n'a pas abouti pour l'adresse:", location])
        maps.close()
        continue

    maps.get_reviews(location, reviews, output_file)

    # Fermer le navigateur pour cette instance
    maps.close()

# Créer un DataFrame Pandas pour les "no match"
df_no_match = pd.DataFrame(no_match, columns=['Erreur', 'Adresse'])

# Stocker les "no match" dans un fichier CSV
df_no_match.to_csv(no_match_file, index=False)
