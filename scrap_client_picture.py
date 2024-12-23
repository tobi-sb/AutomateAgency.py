from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

# Configure browser options
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--enable-logging")
chrome_options.add_argument("--v=1")
chrome_options.add_argument("--log-level=0")
chrome_options.add_argument("--enable-blink-features=NetworkService")
chrome_options.add_argument("--auto-open-devtools-for-tabs")

# Set the logging preferences using set_capability
chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})

# Initialize the Selenium driver without desired_capabilities
browser = webdriver.Chrome(options=chrome_options)

# Ouvrir la page Google Maps
url = "https://www.google.fr/maps/place/AKYOUD+Peinture+peintre+en+b%C3%A2timent/@43.3396737,3.2430455,3a,80.9y,90t/data=!3m8!1e2!3m6!1sAF1QipOSCusQ-ysKE43FpIojp4aHlYQG1e0CyMCh_vCq!2e10!3e12!6shttps:%2F%2Flh5.googleusercontent.com%2Fp%2FAF1QipOSCusQ-ysKE43FpIojp4aHlYQG1e0CyMCh_vCq%3Dw152-h86-k-no!7i1440!8i810!4m7!3m6!1s0x12b10facfc7a81c5:0x9a9808eb8f3233c!8m2!3d43.3395947!4d3.2429831!10e5!16s%2Fg%2F11jly9ygtb?entry=ttu&g_ep=EgoyMDI0MTAyOS4wIKXMDSoASAFQAw%3D%3D"
browser.get(url)

# Accepter les cookies
try:
    cookies_button = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Tout accepter')]")))
    cookies_button.click()
    print("Bouton d'acceptation des cookies cliqué avec succès.")
except Exception as e:
    print(f"Bouton d'acceptation des cookies non trouvé ou non cliquable : {e}")

# Attendre que la page se charge
time.sleep(5)

# Ouvrir un fichier pour enregistrer les sources des images et vidéos
with open('./client_src.txt', 'a') as file:  # Passer en mode 'a' pour ajouter à chaque fois
    # Faire défiler et cliquer sur chaque image avec la classe spécifiée
    already_clicked = set()
    try:
        while True:
            elements = WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "Uf0tqf")))
            elements += browser.find_elements(By.CLASS_NAME, "U39Pmb")  # Ajouter les vidéos
            for element in elements:
                if element in already_clicked:
                    continue
                # Faire défiler l'élément dans la vue
                browser.execute_script("arguments[0].scrollIntoView(true);", element)
                time.sleep(1)
                # Utiliser JavaScript pour cliquer sur l'élément
                try:
                    browser.execute_script("arguments[0].click();", element)
                    print("Élément cliqué avec succès.")
                    already_clicked.add(element)
                    time.sleep(2)
                    # Récupérer toutes les URLs d'images ou de vidéos à partir du réseau
                    network_logs = browser.get_log('performance')
                    for entry in network_logs:
                        log = json.loads(entry['message'])['message']
                        if ('Network.responseReceived' in log['method']) or ('Network.requestWillBeSent' in log['method']):
                            params = log.get('params', {})
                            url = params.get('response', {}).get('url') or params.get('request', {}).get('url')
                            if url and 'https://lh5.googleusercontent.com/' in url:
                                file.write(url + "\n")
                                file.flush()  # Forcer l'écriture immédiate dans le fichier
                                print(f"Source enregistrée : {url}")
                except Exception as e:
                    print(f"Impossible de cliquer sur l'élément : {e}")
            # Faire défiler vers le bas de la page pour charger plus d'éléments
            browser.execute_script("window.scrollBy(0, 1000);")
            time.sleep(3)
    except Exception as e:
        print(f"Impossible de cliquer sur les éléments : {e}")

# Attendre 100 secondes
time.sleep(100)

# Fermer le navigateur
browser.quit()
