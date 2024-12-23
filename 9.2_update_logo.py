import os
import json
from bs4 import BeautifulSoup

# Charger les données du fichier JSON
json_file = './mnt/data/company_1.json'
with open(json_file, 'r', encoding='utf-8') as file:
    company_data = json.load(file)
    new_logo_src = company_data[-1]["content"]  # Le chemin du nouveau logo

# Le dossier où est stocké le site téléchargé
website_dir = './website_downloaded'
images_dir = './images_filter2'
backup_file = './mnt/data/original_sources.json'  # Fichier pour sauvegarder les sources d'origine

# Trouver automatiquement le logo dans le dossier images_filter2
def find_logo_in_images_folder(images_directory):
    for file_name in os.listdir(images_directory):
        if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.svg', '.gif')):
            return file_name  # Retourner uniquement le nom de l'image (sans le chemin complet)
    return None

# Fonction pour sauvegarder les sources d'origine
def save_backup(backup_data):
    with open(backup_file, 'w', encoding='utf-8') as backup:
        json.dump(backup_data, backup, indent=4)

# Fonction pour remplacer les sources de logo dans les fichiers HTML et sauvegarder les anciennes sources
def replace_logo_source_in_html(file_path, logo_name, new_logo, backup_data):
    changes_made = False
    log_entries = []

    # Essayer de lire le fichier HTML avec plusieurs encodages possibles
    encodings_to_try = ['utf-8', 'iso-8859-1', 'latin-1']
    soup = None

    for encoding in encodings_to_try:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                soup = BeautifulSoup(f, 'html.parser')
            break  # Sortir de la boucle si la lecture a réussi
        except UnicodeDecodeError:
            log_entries.append(f"Impossible de lire {file_path} avec l'encodage {encoding}, essai avec un autre encodage.")

    if soup is None:
        log_entries.append(f"Erreur : Impossible de lire {file_path} avec les encodages disponibles.")
        return log_entries

    # Trouver toutes les balises <img> et vérifier si elles contiennent le nom du logo
    for img in soup.find_all('img'):
        img_src = img.get('src')
        if img_src and logo_name in img_src:
            log_entries.append(f"LOGO TROUVÉ dans {file_path}: '{img_src}' sera remplacé par '{new_logo}'")

            # Sauvegarder l'ancienne source dans backup_data
            if file_path not in backup_data:
                backup_data[file_path] = []
            backup_data[file_path].append({'old_src': img_src, 'new_src': new_logo})

            img['src'] = new_logo  # Remplacer la source entière par le nouveau logo
            changes_made = True

    # Si des modifications ont été apportées, enregistrer le fichier mis à jour
    if changes_made:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        log_entries.append(f"Les changements ont été sauvegardés dans {file_path}.")
    else:
        log_entries.append(f"Aucune modification dans {file_path}.")

    return log_entries

    
    # Si des modifications ont été apportées, enregistrer le fichier mis à jour
    if changes_made:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        log_entries.append(f"Les changements ont été sauvegardés dans {file_path}.")
    else:
        log_entries.append(f"Aucune modification dans {file_path}.")

    return log_entries

# Fonction pour parcourir les fichiers HTML du site
def update_logo_in_website(website_directory, logo_name, new_logo):
    
    backup_data = {}  # Dictionnaire pour sauvegarder les anciennes sources
    global_log = []  # Liste pour stocker les logs globaux
    for root, dirs, files in os.walk(website_directory):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                logs = replace_logo_source_in_html(file_path, logo_name, new_logo, backup_data)
                global_log.extend(logs)
    
    # Sauvegarder les anciennes sources dans le fichier JSON
    save_backup(backup_data)

    print("La mise à jour du logo est terminée.")
    return global_log

# Trouver le logo actuel à remplacer
logo_to_replace = find_logo_in_images_folder(images_dir)

if logo_to_replace:
    # Appeler la fonction pour effectuer le remplacement
    log_results = update_logo_in_website(website_dir, logo_to_replace, new_logo_src)

    # Afficher tous les logs
    for log in log_results:
        print(log)

    print(f"Les anciennes sources ont été sauvegardées dans '{backup_file}'.")
    print("Processus terminé.")
else:
    print(f"Aucun fichier logo trouvé dans {images_dir}.")
