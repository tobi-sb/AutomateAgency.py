import os
import json
import re

# Définir les chemins vers les dossiers
json_no_website_path = './json_no_website'
json_blacklist_path = './json_blacklist'

# Récupérer tous les fichiers JSON dans les deux dossiers
json_no_website_files = [f for f in os.listdir(json_no_website_path) if f.endswith('.json')]
json_blacklist_files = [f for f in os.listdir(json_blacklist_path) if f.endswith('.json')]

# Fonction pour extraire les numéros au format "XX XX XX XX XX" d'un fichier JSON
def get_numbers_from_json(file_path):
    numbers = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            for value in data.values():
                if isinstance(value, str):
                    match = re.search(r"\b\d{2} \d{2} \d{2} \d{2} \d{2}\b", value)
                    if match:
                        numbers.append(match.group())
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Erreur dans le fichier {file_path}: {e}")
    return numbers

# Extraire les numéros d'identification de json_blacklist
blacklist_numbers = set()
for filename in json_blacklist_files:
    file_path = os.path.join(json_blacklist_path, filename)
    numbers = get_numbers_from_json(file_path)
    blacklist_numbers.update(numbers)

# Compter et lister les fichiers supprimés
deleted_files = []

# Supprimer les fichiers de json_no_website qui ont le même numéro que ceux de json_blacklist
for filename in json_no_website_files:
    file_path = os.path.join(json_no_website_path, filename)
    numbers = get_numbers_from_json(file_path)
    if any(number in blacklist_numbers for number in numbers):
        os.remove(file_path)
        deleted_files.append(filename)
        print(f'Supprimé : {filename}')
    else:
        print(f'Conservé : {filename}')

# Afficher le nombre total de fichiers supprimés et la liste
print(f"\nTotal de fichiers supprimés : {len(deleted_files)}")
print("Liste des fichiers supprimés :")
for deleted_file in deleted_files:
    print(f"- {deleted_file}")
