import os
import json

# Chemin du dossier principal
website_folder = './website_downloaded'

# Rechercher le dossier qui commence par "www."
subfolders = [f for f in os.listdir(website_folder) if f.startswith("www.") and os.path.isdir(os.path.join(website_folder, f))]
if len(subfolders) == 0:
    print("Aucun dossier commençant par 'www.' n'a été trouvé.")
    exit()

website_subfolder = subfolders[0]
logo_folder = os.path.join(website_folder, website_subfolder, 'logo')

# Vérifier si le dossier logo existe
if not os.path.exists(logo_folder):
    print("Le dossier logo n'existe pas dans le sous-dossier trouvé.")
    exit()

# Obtenir le nom du fichier logo
logo_files = os.listdir(logo_folder)
if len(logo_files) == 0:
    print("Aucun fichier logo trouvé dans le dossier.")
    exit()

logo_file_name = logo_files[0]

# Chemin du fichier JSON
json_file_path = './mnt/data/company_1.json'

# Charger le fichier JSON
with open(json_file_path, 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

# Mettre à jour le nom du fichier logo dans le JSON
for entry in data:
    if entry['type'] == 'logo':
        # Extraire le chemin actuel sans le nom du fichier
        current_path = os.path.dirname(entry['content'])
        # Mettre à jour uniquement le nom du fichier
        entry['content'] = os.path.join(current_path, logo_file_name).replace('\\', '/')

# Sauvegarder les changements dans le fichier JSON
with open(json_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(data, json_file, indent=4, ensure_ascii=False)

print("Le fichier JSON a été mis à jour avec le nouveau nom de fichier logo.")
