import os
import shutil
import time
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException


# Fichier contenant les URLs des sites à capturer
link_file = "./filtered_list.txt"
base_screenshot_folder = "./screenshots"

# Supprimer le contenu du dossier `screenshots` s'il existe
if os.path.exists(base_screenshot_folder):
    shutil.rmtree(base_screenshot_folder)

# Créer le dossier `screenshots` s'il n'existe pas
if not os.path.exists(base_screenshot_folder):
    os.makedirs(base_screenshot_folder)

# Liste des résolutions responsives
responsive_modes = {
    "PC": (1920, 1080),
    "Laptop": (1366, 768),
    "Tablette": (768, 1024),
    "Téléphone": (375, 667)
}

# Charger les URLs depuis le fichier `link.txt`
with open(link_file, 'r') as f:
    urls = [line.strip() for line in f.readlines()]

# Vérifier que les URLs sont valides (ajouter "http://" si manquant)
urls = [url if url.startswith("http") else f"http://{url}" for url in urls]

# Associer chaque URL à son index pour renommer les dossiers
indexed_urls = [(index + 1, url) for index, url in enumerate(urls)]

# Diviser les URLs en 3 parties pour chaque instance
urls_split = [indexed_urls[i::3] for i in range(3)]

# Fonction pour accepter automatiquement les popups de cookies
def accept_cookies(driver):
    try:
        print("Recherche de popup de cookies...")
        cookie_selectors = [
            "//button[text()[contains(., 'Accepter') or contains(., 'Accept') or contains(., 'I Agree') or contains(., 'OK') or contains(., 'Autoriser') or contains(., 'Allow')]]",
            "//button[contains(@id, 'accept') or contains(@id, 'agree') or contains(@id, 'consent') or contains(@id, 'autoriser') or contains(@id, 'allow')]",
            "//button[contains(@class, 'accept') or contains(@class, 'agree') or contains(@class, 'consent') or contains(@class, 'autoriser') or contains(@class, 'allow')]",
            "//button[contains(@aria-label, 'accept') or contains(@aria-label, 'agree') or contains(@aria-label, 'consent') or contains(@aria-label, 'autoriser') or contains(@aria-label, 'allow')]",
            "//div[contains(@class, 'cookie-consent')]//button",
            "//input[@type='submit' and (contains(@value, 'Accept') or contains(@value, 'I Agree') or contains(@value, 'Autoriser') or contains(@value, 'Allow'))]",
            "//*[contains(text(), 'Accept All') or contains(text(), 'Accept Cookies') or contains(text(), 'I Agree') or contains(text(), 'Accepter tous') or contains(text(), 'Autoriser tous') or contains(text(), 'Allow All')]",
            "//a[contains(@class, 'accept') or contains(@class, 'agree') or contains(@class, 'consent') or contains(@class, 'autoriser') or contains(@class, 'allow')]",
            "//button[@title='Accept' or @title='Autoriser' or @title='Allow']",
            "//*[contains(@role, 'button') and (contains(text(), 'Accepter') or contains(text(), 'Accept') or contains(text(), 'I Agree') or contains(text(), 'OK') or contains(text(), 'Autoriser') or contains(text(), 'Allow'))]",
            "//button[@data-rgpdaction='accept-rgpd-modal']",
            "//button[contains(@data-rgpdaction, 'accept') or contains(@data-rgpdaction, 'consent')]",
            "//*[contains(@label, 'Accepter') or contains(@label, 'Autoriser') or contains(@label, 'Accept') or contains(@label, 'Allow')]"
        ]

        # Basculer dans chaque iframe pour rechercher les popups de cookies
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        for index, iframe in enumerate(iframes):
            try:
                # Timeout pour chaque iframe (par exemple 5 secondes)
                WebDriverWait(driver, 5).until(EC.frame_to_be_available_and_switch_to_it(iframe))
                print(f"Vérification de l'iframe {index + 1} sur {len(iframes)} pour le popup de cookies...")
                if check_and_accept_cookies(driver, cookie_selectors):
                    driver.switch_to.default_content()
                    return True  # Le bouton de consentement a été trouvé et cliqué
            except TimeoutException:
                print(f"L'iframe {index + 1} a pris trop de temps à charger, passage au suivant.")
            driver.switch_to.default_content()  # Revenir au contenu principal si rien n'est trouvé dans l'iframe

        print("Aucun bouton de consentement trouvé dans les iframes, vérification sur la page principale...")
        return check_and_accept_cookies(driver, cookie_selectors)

    except Exception as e:
        print(f"Erreur lors de la gestion des popups de cookies : {e}")
        return False

# Fonction de vérification et clic sur le bouton d'acceptation des cookies
def check_and_accept_cookies(driver, cookie_selectors):
    try:
        for selector in cookie_selectors:
            elements = driver.find_elements(By.XPATH, selector)
            if elements:
                for element in elements:
                    if element.is_displayed():
                        try:
                            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, selector)))
                            element.click()
                            print(f"Bouton de consentement trouvé et cliqué : {selector}")
                            return True
                        except (TimeoutException, NoSuchElementException) as e:
                            print(f"Erreur lors du clic sur le bouton : {e}")
        return False
    except Exception as e:
        print(f"Erreur lors de la recherche du bouton de consentement : {e}")
        return False

# Fonction pour capturer des captures d'écran pour chaque URL
def capture_screenshots(indexed_urls, instance_id):
    # Configuration initiale de Selenium
    options = Options()
    options.binary_location = r"C:\chrome-win64\chrome.exe"
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-web-security")
    options.add_argument("--allow-running-insecure-content")
    options.add_argument(f"--remote-debugging-port={9222 + instance_id}")
    options.add_argument("--incognito")
    options.add_argument("--user-agent=Mozilla/5.0")

    # Utilisation de WebDriverManager pour charger Chrome automatiquement
    driver = webdriver.Chrome(service=ChromeService(r"C:\chrome_driver\chromedriver.exe"), options=options)


    for index, url in indexed_urls:
        print(f"Instance {instance_id}: Capture de l'URL {url}")
        driver.get(url)
        accept_cookies(driver)  # Appeler la fonction pour accepter les cookies
        time.sleep(2)  # Attendre que la page soit chargée
        screenshot_folder = os.path.join(base_screenshot_folder, f"{index}_{url.replace('http://', '').replace('https://', '').replace('/', '_')}")
        if not os.path.exists(screenshot_folder):
            os.makedirs(screenshot_folder)

        # Capturer des captures d'écran pour chaque mode responsive
        for mode, (width, height) in responsive_modes.items():
            driver.set_window_size(width, height)
            time.sleep(1)  # Attendre que la page s'adapte à la nouvelle taille
            mode_folder = os.path.join(screenshot_folder, mode)
            if not os.path.exists(mode_folder):
                os.makedirs(mode_folder)

            scroll_height = driver.execute_script("return document.body.scrollHeight")
            scroll_position = 0
            screenshot_index = 1

            while scroll_position < scroll_height:
                screenshot_path = os.path.join(mode_folder, f"screenshot_{screenshot_index}.png")
                driver.save_screenshot(screenshot_path)
                scroll_position += height
                driver.execute_script(f"window.scrollTo(0, {scroll_position});")
                time.sleep(0.5)
                screenshot_index += 1

            # Capturer le bas de la page
            driver.execute_script(f"window.scrollTo(0, {scroll_height});")
            screenshot_path = os.path.join(mode_folder, f"screenshot_{screenshot_index}.png")
            driver.save_screenshot(screenshot_path)
            print(f"Instance {instance_id}: Capture d'écran enregistrée : {screenshot_path}")

    # Fermer le navigateur
    driver.quit()

# Lancer 3 threads pour chaque instance
threads = []
for i in range(3):
    thread = threading.Thread(target=capture_screenshots, args=(urls_split[i], i))
    threads.append(thread)
    thread.start()

# Attendre que tous les threads soient terminés
for thread in threads:
    thread.join()