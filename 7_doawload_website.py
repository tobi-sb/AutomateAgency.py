import os
import shutil
import subprocess
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import logging

# Configuration du logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', filename='download_log.log', filemode='w')
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logging.getLogger().addHandler(console_handler)

# Chemins des fichiers et dossiers
input_file = './final_website_rank.txt'
download_folder = './website_downloaded'
images_folder = './website_downloaded/images_extracted'

# Vider le dossier de téléchargement
def clear_download_folder(folder_path):
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
    os.makedirs(folder_path)
    logging.info(f"Dossier de téléchargement vidé et recréé : {folder_path}")

# Vider le dossier des images
def clear_images_folder(folder_path):
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
    os.makedirs(folder_path)
    logging.info(f"Dossier des images vidé et recréé : {folder_path}")

# Lire les URLs à partir du fichier
def read_urls(file_path):
    with open(file_path, 'r') as file:
        urls = [line.strip() for line in file.readlines() if line.strip()]
    logging.info(f"URLs lues depuis le fichier {file_path}: {urls}")
    return urls

# Télécharger le site avec httrack
def download_website(url, download_path):
    command = [
        'httrack',
        url,
        '--mirror',
        '--depth=3',  # Téléchargement complet avec une profondeur de 3 (vous pouvez ajuster si nécessaire)
        '--ext-depth=3',  # Téléchargement des ressources externes avec une profondeur de 3
        '--path', download_path,
        '--robots=0'  # Ignorer le fichier robots.txt
    ]
    logging.info(f"Commande httrack exécutée : {' '.join(command)}")
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    logging.info(f"Sortie httrack :\n{result.stdout}")
    print(result.stdout)  # Afficher la sortie de httrack en direct dans la console
    logging.info(f"Résultat de httrack : Code de retour {result.returncode}")
    return result.returncode == 0

# Télécharger les images manquantes
def download_missing_images(url, download_path, images_path):
    clear_images_folder(images_path)
    html_files = [os.path.join(root, file) for root, _, files in os.walk(download_path) for file in files if file.endswith('.html')]
    logging.info(f"Fichiers HTML trouvés pour le traitement des images : {html_files}")
    
    downloaded_images = set()  # Pour suivre les images déjà téléchargées
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    
    for html_file in html_files:
        with open(html_file, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')
            images = soup.find_all('img')
            logging.info(f"Images trouvées dans le fichier {html_file} : {[img.get('src') for img in images]}")
            
            for img in images:
                img_url = img.get('src')
                if img_url:
                    # Nettoyer l'URL en supprimant les paramètres après le symbole '#'
                    img_url = img_url.split('#')[0]
                    parsed_url = urlparse(img_url)
                    if not parsed_url.scheme:
                        full_url = urljoin(url, img_url)
                    else:
                        full_url = img_url
                    
                    if full_url in downloaded_images:
                        logging.info(f"Image déjà téléchargée, ignorée : {full_url}")
                        continue
                    
                    retries = 3
                    for attempt in range(retries):
                        try:
                            response = requests.get(full_url, stream=True, timeout=20, headers=headers)  # Augmenter le timeout pour améliorer les chances de succès
                            if response.status_code == 200:
                                img_extension = os.path.splitext(parsed_url.path)[-1]
                                if img_extension not in ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp']:
                                    img_extension = '.jpg'  # Défaut à jpg si l'extension est manquante ou non standard
                                img_filename = os.path.basename(parsed_url.path) or f"image_{int(time.time())}{img_extension}"
                                img_path = os.path.join(images_path, img_filename)
                                with open(img_path, 'wb') as img_file:
                                    shutil.copyfileobj(response.raw, img_file)
                                # Mettre à jour la source de l'image dans le fichier HTML
                                img['src'] = os.path.relpath(img_path, os.path.dirname(html_file)).replace('\\', '/')
                                logging.info(f"Image téléchargée avec succès : {full_url} vers {img_path}")
                                downloaded_images.add(full_url)
                                break
                            else:
                                logging.warning(f"Erreur lors du téléchargement de l'image {full_url}: Statut {response.status_code}")
                                # Essayer avec une autre extension si l'image retourne une erreur 404
                                if response.status_code == 404:
                                    possible_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp']
                                    for ext in possible_extensions:
                                        alternative_url = os.path.splitext(full_url)[0] + ext
                                        if alternative_url != full_url:
                                            response = requests.get(alternative_url, stream=True, timeout=20, headers=headers)
                                            if response.status_code == 200:
                                                img_extension = ext
                                                img_filename = os.path.basename(parsed_url.path) or f"image_{int(time.time())}{img_extension}"
                                                img_path = os.path.join(images_path, img_filename)
                                                with open(img_path, 'wb') as img_file:
                                                    shutil.copyfileobj(response.raw, img_file)
                                                # Mettre à jour la source de l'image dans le fichier HTML
                                                img['src'] = os.path.relpath(img_path, os.path.dirname(html_file)).replace('\\', '/')
                                                logging.info(f"Image téléchargée avec succès (alternative) : {alternative_url} vers {img_path}")
                                                downloaded_images.add(alternative_url)
                                                break
                        except requests.RequestException as e:
                            logging.error(f"Erreur lors du téléchargement de l'image {full_url}: {e}")
                        except Exception as e:
                            logging.error(f"Erreur inattendue lors du téléchargement de l'image {full_url}: {e}")
                        time.sleep(1)  # Attendre avant de réessayer
                    else:
                        logging.error(f"Échec du téléchargement de l'image {full_url} après {retries} tentatives")
                    time.sleep(0.2)  # Réduire le délai pour accélérer le téléchargement des images
        # Enregistrer les modifications apportées au fichier HTML
        with open(html_file, 'w', encoding='utf-8') as file:
            file.write(str(soup))
            logging.info(f"Modifications enregistrées dans le fichier HTML : {html_file}")

# Vérifier le contenu téléchargé
def check_downloaded_content(download_path):
    total_files = sum(len(files) for _, _, files in os.walk(download_path))
    image_files = [file for root, _, files in os.walk(download_path) for file in files if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp'))]
    total_images = len(image_files)
    logging.info(f"Vérification du contenu téléchargé : Total des fichiers = {total_files}, Total des images = {total_images}")
    
    return total_files > 8 and total_images > 5

# Fonction principale
def main():
    urls = read_urls(input_file)
    
    if urls:
        url = urls[0]
        logging.info(f'Téléchargement de : {url}')
        clear_download_folder(download_folder)
        success = download_website(url, download_folder)
        
        if success:
            logging.info(f'Téléchargement terminé pour : {url}')
            logging.info('Téléchargement des images manquantes...')
            try:
                download_missing_images(url, download_folder, images_folder)
                logging.info('Téléchargement des images manquantes terminé.')
            except Exception as e:
                logging.error(f"Erreur lors du téléchargement des images manquantes : {e}")
            
            if check_downloaded_content(download_folder):
                logging.info(f'Téléchargement réussi pour : {url}')
            else:
                logging.warning(f'Téléchargement incomplet pour : {url}, lancement de ./7.2_wcopy.py')
                subprocess.run(['python', './7.2_wcopy.py'])
        else:
            logging.error(f'Échec du téléchargement pour : {url}, lancement de ./7.2_wcopy.py')
            subprocess.run(['python', './7.2_wcopy.py'])
    else:
        logging.error("Aucune URL trouvée dans le fichier d'entrée.")

if __name__ == '__main__':
    main()
