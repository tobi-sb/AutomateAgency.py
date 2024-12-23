# Script pour télécharger les images à partir des liens dans ./client_src en utilisant le multithreading

import os
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

def download_image(url, idx, download_folder):
    url = url.strip()
    if url:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                # Déterminer le nom du fichier
                file_name = os.path.join(download_folder, f'image_{idx + 1}.jpg')
                # Enregistrer l'image
                with open(file_name, 'wb') as img_file:
                    img_file.write(response.content)
                print(f"Téléchargé : {file_name}")
            else:
                print(f"Échec du téléchargement (statut {response.status_code}) : {url}")
        except Exception as e:
            print(f"Erreur lors du téléchargement de {url} : {e}")

def download_images(file_path, download_folder):
    # Créer le dossier de téléchargement s'il n'existe pas
    os.makedirs(download_folder, exist_ok=True)

    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Utiliser ThreadPoolExecutor pour le multithreading
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for idx, url in enumerate(lines):
            # Soumettre la tâche de téléchargement à l'exécuteur
            futures.append(executor.submit(download_image, url, idx, download_folder))

        # Optionnel : attendre que toutes les tâches soient terminées
        for future in as_completed(futures):
            pass  # Vous pouvez gérer les exceptions ici si nécessaire

if __name__ == "__main__":
    download_images('./client_src.txt', './image_src_download')
