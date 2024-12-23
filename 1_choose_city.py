import json
import random
import geopy.distance

# Fonction pour obtenir les coordonnées d'une ville dans FR_unique.txt
def get_city_coordinates(city_name, file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.split('\t')
            if len(parts) > 10 and parts[2].strip().lower() == city_name.strip().lower():
                return float(parts[9]), float(parts[10])  # Latitude, Longitude
    raise ValueError(f"Ville {city_name} non trouvée dans {file_path}.")

# Lire le fichier JSON pour obtenir la ville
with open('./mnt/data/company_1.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)
    city_json = None
    for item in data:
        if item["type"] == "nom de ville":
            city_json = item["content"]
            break

if city_json:
    try:
        # Obtenir les coordonnées de la ville du JSON à partir de FR_unique.txt
        city_json_coordinates = get_city_coordinates(city_json, './FR_unique.txt')
    except ValueError as e:
        print(f"Erreur: {e}")
        exit()

    # Lire toutes les villes et leurs coordonnées de FR_unique.txt
    with open('./FR_unique.txt', 'r', encoding='utf-8') as city_file:
        cities = city_file.readlines()

    eligible_cities = []
    for city in cities:
        parts = city.split('\t')
        if len(parts) > 10:
            city_name = parts[2]
            city_coordinates = (float(parts[9]), float(parts[10]))  # Latitude, Longitude
            
            # Calculer la distance entre la ville du JSON et cette ville
            distance = geopy.distance.geodesic(city_json_coordinates, city_coordinates).km
            if distance > 100:
                eligible_cities.append(city_name)

    # Sélectionner 6 villes au hasard parmi celles à plus de 100 km
    if len(eligible_cities) >= 6:
        random_cities = random.sample(eligible_cities, 6)
        print("Les 6 villes choisies à plus de 100 km sont :", random_cities)

        # Enregistrer les villes sélectionnées dans ./city.txt (écrase le fichier s'il existe)
        with open('./city.txt', 'w', encoding='utf-8') as output_file:
            for city in random_cities:
                output_file.write(city + '\n')

        print(f"Les villes sélectionnées ont été enregistrées dans ./city.txt.")
    else:
        print("Pas assez de villes disponibles à plus de 100 km.")
else:
    print("Ville non trouvée dans le fichier JSON.")
