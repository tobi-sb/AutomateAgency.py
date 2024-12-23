import os
import json
import shutil

# Définir les chemins des dossiers
json_folder = './json'
output_folder = './json_no_website'

# Créer le dossier de sortie s'il n'existe pas
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Parcourir tous les fichiers JSON dans le dossier spécifié
for filename in os.listdir(json_folder):
    if filename.endswith('.json'):
        file_path = os.path.join(json_folder, filename)
        
        # Ouvrir et lire le contenu du fichier JSON
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            
            # Vérifier si l'élément 'element_2' existe et s'il ne contient pas de site web
            website = data.get('element_2', '').lower()
            if not website or 'instagram.com' in website or 'facebook.com' in website:
                # Copier le fichier dans le dossier de sortie
                shutil.copy(file_path, os.path.join(output_folder, filename))

print("Les fichiers JSON sans site web ont été copiés dans le dossier ./json_no_website")
