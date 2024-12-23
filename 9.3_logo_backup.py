import os
import json
from bs4 import BeautifulSoup

# Le dossier où est stocké le site téléchargé
website_dir = './website_downloaded'
backup_file = './mnt/data/original_sources.json'  # Fichier avec les anciennes sources sauvegardées

# Charger le fichier de sauvegarde
def load_backup(backup_file):
    if os.path.exists(backup_file):
        with open(backup_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        return {}

# Fonction pour restaurer les sources d'origine dans les fichiers HTML
def restore_original_sources(backup_data):
    for file_path, images in backup_data.items():
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f, 'html.parser')

            changes_made = False
            for img in soup.find_all('img'):
                img_src = img.get('src')
                for image_data in images:
                    if img_src == image_data['new_src']:  # Vérifier si l'image a été modifiées
                        img['src'] = image_data['old_src']
                        changes_made = True

            if changes_made:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(str(soup))
                print(f"Les changements ont été sauvegardés dans {file_path}.")
            else:
                print(f"Aucune modification dans {file_path}.")
        else:
            print(f"Fichier non trouvé: {file_path}")

# Charger les données de sauvegarde
backup_data = load_backup(backup_file)

# Restaurer les sources d'origine
if backup_data:
    restore_original_sources(backup_data)
    print("Restauration terminée.")
else:
    print(f"Aucune donnée de sauvegarde trouvée dans {backup_file}.")
