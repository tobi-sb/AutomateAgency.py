import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image
import time

# Fonction pour trouver le bon fichier index.html dans les sous-dossiers
def find_index_html(start_dir):
    for root, dirs, files in os.walk(start_dir):
        if 'index.html' in files and root != start_dir:  # ignorer l'index.html dans la racine
            return os.path.join(root, 'index.html')
    return None

# Fonction pour obtenir un chemin absolu
def get_absolute_file_url(relative_path):
    return f"file://{os.path.abspath(relative_path)}"

# Initialiser le navigateur et capturer les premiers 25% de la page pour mobile et pc
def open_browser_and_capture_top_25vh(html_path):
    # Setup du driver Chrome
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(r"C:\chrome_driver\chromedriver.exe"), options=options)

    
    # Charger le fichier HTML avec un chemin absolu
    file_url = get_absolute_file_url(html_path)
    driver.get(file_url)
    
    # Attendre que la page se charge
    time.sleep(2)

    # Liste des configurations de capture d'écran
    device_configs = [
        {"name": "mobile", "window_size": (375, 812)},
        {"name": "pc", "window_size": (1920, 1080)}
    ]

    for config in device_configs:
        # Définir la taille de la fenêtre
        driver.set_window_size(config["window_size"][0], config["window_size"][1])
        
        # Attendre un moment après le redimensionnement
        time.sleep(1)

        # Obtenir les dimensions de la fenêtre de la page
        window_width = driver.execute_script("return window.innerWidth")
        window_height = driver.execute_script("return window.innerHeight")

        # Calculer 25% de la hauteur de la fenêtre
        crop_height = int(0.25 * window_height)
        time.sleep(4)


        # Prendre une capture d'écran de la page entière
        screenshot_name = f'full_screenshot_{config["name"]}.png'
        driver.save_screenshot(screenshot_name)

        # Ouvrir l'image entière
        image = Image.open(screenshot_name)

        # Découper la partie supérieure de l'image (25% de la hauteur de la fenêtre)
        top_image = image.crop((0, 0, window_width, crop_height))

        # Sauvegarder l'image découpée
        cropped_image_name = f'./website_downloaded/img_before_after_nav/nav-screen-{config["name"]}.png'
        top_image.save(cropped_image_name)
        print(f"Capture d'écran des premiers 25% de la page enregistrée pour {config['name']} !")

    driver.quit()

# Exemple d'exécution
website_folder = './website_downloaded'
index_html_path = find_index_html(website_folder)

if index_html_path:
    print(f"Fichier index.html trouvé : {index_html_path}")
    open_browser_and_capture_top_25vh(index_html_path)
else:
    print("Aucun fichier index.html trouvé dans les sous-dossiers.")
