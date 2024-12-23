from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import time
import json
import os
import multiprocessing
import datetime
import tensorflow as tf

# Charger le fichier combined_output.txt
with open('./combined_output.txt', 'r', encoding='latin-1') as combined_file:
    combined_entries = combined_file.readlines()

# Créer le dossier ./json s'il n'existe pas
if not os.path.exists('./json'):
    os.makedirs('./json')
    print("Dossier ./json créé.")

def worker(entries, instance_id, avg_time_per_json):
    # Configuration du driver Selenium en mode headless
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--disable-software-rasterizer")  # Utiliser le GPU autant que possible
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    browser = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(browser, 10)

    def scroll_into_view(element):
        browser.execute_script("arguments[0].scrollIntoView(true);", element)

    def scroll_down():
        browser.execute_script("window.scrollBy(0, 1000);")

    try:
        total_tasks = len(entries) * 20
        completed_tasks = 0
        start_time = datetime.datetime.now()

        for entry in entries:
            entry = entry.strip()
            # Ouvrir Google Maps
            print(f"Instance {instance_id}: Ouverture de Google Maps pour {entry}...")
            browser.get("https://www.google.com/maps")

            # Accepter les cookies si le bouton est présent
            try:
                accept_cookies_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Tout accepter']")))
                accept_cookies_button.click()
                print(f"Instance {instance_id}: Bouton 'Tout accepter' cliqué.")
            except:
                print(f"Instance {instance_id}: Bouton 'Tout accepter' non trouvé.")

            # Trouver la barre de recherche et entrer la catégorie et la ville
            try:
                print(f"Instance {instance_id}: Recherche de la barre de recherche...")
                search_bar = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='searchboxinput']")))
                search_bar.send_keys(entry)
                search_bar.send_keys(Keys.ENTER)
                print(f"Instance {instance_id}: Recherche lancée pour: {entry}")
            except:
                print(f"Instance {instance_id}: Barre de recherche non trouvée.")
                continue

            # Attendre que les résultats se chargent
            time.sleep(2)

            # Parcourir les fiches Google Business (20 au total)
            for i in range(20):
                try:
                    print(f"Instance {instance_id}: Récupération de la fiche Google Business {i + 1}...")
                    business_cards = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.Nv2PK")))
                    if i < len(business_cards):
                        card = business_cards[i]
                        scroll_into_view(card)
                        action = ActionChains(browser)
                        action.move_to_element(card).click().perform()
                        time.sleep(2)  # Attendre que la vue détaillée se charge

                        # Attendre que la nouvelle div apparaisse après avoir cliqué sur la fiche
                        business_info = {}
                        try:
                            details_divs = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='AeaXub']")))
                            for index, div in enumerate(details_divs):
                                text = div.text.strip()
                                business_info[f"element_{index + 1}"] = text.replace('\n', ' ')
                                print(f"Instance {instance_id}: Élément {index + 1} trouvé avec la classe 'AeaXub'. Texte : {text}")
                        except Exception as e:
                            print(f"Instance {instance_id}: Aucun élément trouvé après clic sur la fiche - {str(e)}")
                            # Passer à la fiche suivante sans retour en arrière
                            continue

                        # Récupérer le texte de l'élément h1 spécifié
                        try:
                            header_element = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='QA0Szd']/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div/div[1]/div[1]/h1")))
                            business_info["header"] = header_element.text.strip()
                            print(f"Instance {instance_id}: Titre trouvé: {header_element.text.strip()}")
                        except Exception as e:
                            print(f"Instance {instance_id}: Titre non trouvé - {str(e)}")

                        # Sauvegarder les informations de la fiche dans un fichier JSON individuel
                        json_filename = f"./json/{entry}_business_{i + 1}_instance_{instance_id}.json".replace(" ", "_")
                        with open(json_filename, 'w', encoding='utf-8') as json_file:
                            json.dump(business_info, json_file, ensure_ascii=False, indent=4)
                        print(f"Instance {instance_id}: Données sauvegardées dans {json_filename}")

                        # Mise à jour des tâches terminées et estimation du temps restant
                        completed_tasks += 1
                        elapsed_time = (datetime.datetime.now() - start_time).total_seconds()
                        estimated_total_time = (elapsed_time / completed_tasks) * total_tasks
                        remaining_time = estimated_total_time - elapsed_time
                        print(f"Instance {instance_id}: Temps restant estimé: {remaining_time / 60:.2f} minutes")

                        # Retourner en arrière pour revenir aux résultats
                        try:
                            back_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='omnibox-singlebox']/div/div[1]/button/span")))
                            back_button.click()
                            print(f"Instance {instance_id}: Bouton retour cliqué.")
                        except Exception as e:
                            print(f"Instance {instance_id}: Erreur lors du clic sur le bouton retour - {str(e)}")
                        time.sleep(2)  # Attendre que la page précédente se recharge
                    else:
                        print(f"Instance {instance_id}: Fiche {i + 1} non trouvée.")
                        break

                except Exception as e:
                    print(f"Instance {instance_id}: Erreur lors de la récupération de la fiche {i + 1} - {str(e)}")

            # Faire défiler la page vers le bas pour charger plus de fiches si disponible
            for _ in range(5):  # Scroll plusieurs fois pour charger plus de résultats
                scroll_down()
                time.sleep(2)

            # Supprimer l'entrée traitée du fichier
            with open('./combined_output.txt', 'r', encoding='latin-1') as combined_file:
                lines = combined_file.readlines()
            with open('./combined_output.txt', 'w', encoding='latin-1') as combined_file:
                for line in lines:
                    if line.strip() != entry:
                        combined_file.write(line)

    finally:
        # Fermer le navigateur
        print(f"Instance {instance_id}: Fermeture du navigateur...")
        browser.quit()

if __name__ == "__main__":
    # Diviser les entrées en 4 parts pour 4 instances
    num_instances = 4
    entries_split = [combined_entries[i::num_instances] for i in range(num_instances)]

    # Temps moyen estimé par fiche (en secondes)
    avg_time_per_json = 15  # Ajuster en fonction de l'expérience

    # Créer des processus pour chaque instance
    processes = []
    for i in range(num_instances):
        p = multiprocessing.Process(target=worker, args=(entries_split[i], i + 1, avg_time_per_json))
        processes.append(p)
        p.start()

    # Attendre que tous les processus se terminent
    for p in processes:
        p.join()
