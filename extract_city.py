import requests
import time

# Liste des 5 villes pour le test
cities = [
    "Paris", "Marseille", "Lyon", "Toulouse", "Nice" 
]

# URL de l'API Nominatim
nominatim_url = "https://nominatim.openstreetmap.org/search"

# Fonction pour récupérer les coordonnées d'une ville
def get_city_coordinates(city):
    params = {
        'q': city,
        'format': 'json',
        'limit': 1,
        'addressdetails': 1  # Pour s'assurer que l'adresse est bien détaillée
    }
    try:
        response = requests.get(nominatim_url, params=params)
        response.raise_for_status()  # Lève une erreur pour les statuts non 200
        data = response.json()
        if data:
            lat = data[0]['lat']
            lon = data[0]['lon']
            return lat, lon
        else:
            print(f"Aucune donnée pour {city}")
    except requests.exceptions.HTTPError as http_err:
        print(f"Erreur HTTP pour {city}: {http_err}")
    except Exception as e:
        print(f"Erreur pour {city}: {e}")
    return None, None

# Fichier pour enregistrer les résultats
output_file = "cities_with_coordinates_test.txt"

# Boucle pour récupérer les coordonnées de chaque ville
with open(output_file, "w") as file:
    for city in cities:
        lat, lon = get_city_coordinates(city)
        if lat and lon:
            file.write(f"{city}: {lat}, {lon}\n")
        else:
            file.write(f"{city}: Coordonnées non trouvées\n")
        # Pause pour éviter de surcharger l'API
        time.sleep(1)

print(f"Coordonnées enregistrées dans {output_file}")
