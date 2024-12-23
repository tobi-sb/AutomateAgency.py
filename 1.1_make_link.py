from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import json
import random
from threading import Thread

# Charger le fichier JSON
file_path = "./mnt/data/company_1.json"
with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Extraire la catégorie et la ville actuelle
category = None
current_city = None

for item in data:
    if item['type'] == 'categorie':
        category = item['content']
    elif item['type'] == 'nom de ville':
        current_city = item['content']

# Vérifier que les informations ont bien été récupérées
if not category or not current_city:
    raise ValueError("Le fichier JSON ne contient pas les informations de catégorie ou de ville requises.")

# Lire les villes depuis le fichier ./city.txt
city_file_path = "./city.txt"
with open(city_file_path, 'r', encoding='utf-8') as city_file:
    far_cities = [line.strip() for line in city_file.readlines() if line.strip()]

# Vérifier si nous avons trois villes
if len(far_cities) != 6:
    raise ValueError("Le fichier city.txt doit contenir exactement quatre villes.")

# Afficher les villes choisies
print(f"Villes choisies : {', '.join(far_cities)}")

# Fonction pour effectuer la recherche et enregistrer les liens
def search_and_collect_links(city, category, all_links):
    # Configuration du driver Selenium (par exemple, chromedriver)
    driver = webdriver.Chrome()

    try:
        # Ouvre Google
        driver.get("https://www.google.com")

        # Attend un court moment pour s'assurer que la page est bien chargée
        time.sleep(3)

        # Clique sur l'élément avec les classes .QS5gu.sy4vM (par exemple, bouton "J'accepte" pour les cookies)
        try:
            element = driver.find_element(By.CSS_SELECTOR, ".QS5gu.sy4vM")
            ActionChains(driver).move_to_element(element).click().perform()
            time.sleep(2)
        except:
            pass  # Ignore s'il ne trouve pas le bouton des cookies

        # Trouve la barre de recherche avec l'attribut name='q'
        search_bar = driver.find_element(By.NAME, "q")

        # Écrit la recherche basée sur la catégorie et la ville éloignée
        search_query = f"{category} {city}"
        search_bar.send_keys(search_query)
        search_bar.send_keys(Keys.RETURN)

        # Attend que la page se charge
        time.sleep(3)

        # Parcourt plusieurs pages de résultats jusqu'à ce que 40 liens soient collectés pour chaque ville
        links_collected = 0
        city_links = []
        while links_collected < 40:
            # Effectue un scroll vers le bas de la page pour charger plus de résultats
            for _ in range(3):
                driver.execute_script("window.scrollBy(0, 1000);")
                time.sleep(2)  # Attend un peu pour laisser les nouveaux résultats se charger

            # Récupère les résultats de recherche de sites (exclut les Google Fiches)
            results = driver.find_elements(By.CSS_SELECTOR, "div.yuRUbf a")

            # Récupère les URL des résultats (évite les fiches locales ou liens sponsorisés)
            links = [result.get_attribute('href') for result in results]
            city_links.extend(links)
            city_links = list(dict.fromkeys(city_links))  # Supprime les doublons
            links_collected = len(city_links)

            # Passe à la page suivante si possible
            if links_collected < 40:
                try:
                    next_button = driver.find_element(By.ID, "pnnext")
                    next_button.click()
                    time.sleep(3)  # Attend que la page suivante se charge
                except:
                    print("Aucune page suivante trouvée.")
                    break

        # Ajouter les liens collectés pour la ville actuelle à la liste globale
        all_links.extend(city_links[:40])
    finally:
        # Ferme le navigateur
        driver.quit()

all_links = []

# Lance les recherches sur les trois villes en parallèle
def thread_function(city, category, all_links):
    search_and_collect_links(city, category, all_links)

threads = []
for city in far_cities:
    thread = Thread(target=thread_function, args=(city, category, all_links))
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

# Enregistre les liens dans un fichier texte
with open("link.txt", "w") as file:
    for link in all_links:
        file.write(link + "\n")

# Affiche le contenu de link.txt
print(f"Les liens sont enregistrés dans 'link.txt' :\n{all_links}")

# Attend 10 secondes pour observer le résultat
time.sleep(3)
