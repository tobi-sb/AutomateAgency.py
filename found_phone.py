import json
import glob

# Charger tous les fichiers JSON dans le dossier ./json_blacklist
json_files = glob.glob("./json/*.json")

# Demander le numéro de téléphone à chercher
search_number = input("Entrez le numéro de téléphone que vous souhaitez rechercher (format : XX XX XX XX XX) : ")

# Fonction pour vérifier si un numéro est dans un fichier JSON
def find_json_with_number(search_number, json_files):
    for file in json_files:
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Vérifier tous les éléments du fichier pour trouver le numéro
            for key, value in data.items():
                if search_number in value:
                    return file, data
    return None, None

# Recherche du fichier correspondant
file_found, data_found = find_json_with_number(search_number, json_files)

if data_found:
    print(f"Le fichier correspondant est : {file_found}")
    print(json.dumps(data_found, indent=4, ensure_ascii=False))
else:
    print("Numéro non trouvé dans les fichiers JSON.")
