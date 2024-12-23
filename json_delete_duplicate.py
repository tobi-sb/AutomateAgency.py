import json
import os

# Fonction pour traiter les fichiers JSON
def process_json_files(json_files):
    json_data_list = []
    json_file_map = {}

    # Charger tous les fichiers JSON
    for json_file in json_files:
        with open(json_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
            print(f"Chargement du fichier : {json_file}")
            json_data_list.append((json_file, data))

    # Supprimer les doublons en utilisant une approche basée sur les hachages
    seen_hashes = set()

    for json_file, data in json_data_list:
        data_hash = hash(json.dumps(data, sort_keys=True))
        if data_hash not in seen_hashes:
            print(f"JSON unique trouvé et conservé : {json_file}")
            seen_hashes.add(data_hash)
        else:
            print(f"JSON en double supprimé : {json_file}")
            os.remove(json_file)

# Liste des fichiers JSON à traiter
json_directory = './json_no_website'
json_files = [os.path.join(json_directory, f) for f in os.listdir(json_directory) if f.endswith('.json')]

# Traitement des fichiers JSON
process_json_files(json_files)

print("Traitement terminé.")