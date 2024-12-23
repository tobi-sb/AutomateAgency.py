from bs4 import BeautifulSoup
import os
import re
import urllib.parse
import shutil
from collections import Counter

# Dossiers contenant le site internet et les images
site_folder = './website_downloaded'
images_folder = './images_filter1'
output_folder = './images_filter2'

# Effacer le contenu du dossier de sortie s'il existe
if os.path.exists(output_folder):
    shutil.rmtree(output_folder)

# Créer le dossier de sortie s'il n'existe pas
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Charger les noms des images du dossier en minuscules (sans extension)
image_names = [os.path.splitext(img.lower())[0] for img in os.listdir(images_folder) if img.endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg'))]
print(f"Noms des images chargées : {image_names}")

# Fonction pour normaliser un nom d'image (enlever les caractères spéciaux, underscores, etc.)
def normalize_name(name):
    return re.sub(r'[^a-zA-Z0-9]', '', name.lower())

# Dictionnaire pour stocker la position de chaque image trouvée
image_positions = {}

# Fonction pour analyser un fichier HTML
def analyze_file(file_path, image_names):
    try:
        print(f"Analyse du fichier : {file_path}")
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            soup = BeautifulSoup(f, 'html.parser')
            
            # Chercher toutes les balises <img>, <meta> et autres potentiellement contenant des images
            img_tags = soup.find_all(['img', 'meta', 'link'])
            relevant_tags = []

            for tag in img_tags:
                if tag.name == 'img' and tag.get('src'):
                    relevant_tags.append(tag['src'])
                elif tag.name == 'meta' and tag.get('content') and (tag.get('property') in ['og:image', 'twitter:image'] or tag.get('name') in ['og:image', 'twitter:image']):
                    relevant_tags.append(tag['content'])
                elif tag.name == 'link' and tag.get('href') and ('icon' in tag.get('rel', [])):
                    relevant_tags.append(tag['href'])

            # Parcourir les balises pertinentes et vérifier les correspondances
            for position, src in enumerate(relevant_tags):
                parsed_src = urllib.parse.urlparse(src).path  # Extraire uniquement le chemin du src
                parsed_src_name = os.path.splitext(os.path.basename(parsed_src))[0].lower()  # Extraire le nom du fichier sans l'extension et le mettre en minuscule
                
                # Normaliser les noms pour la comparaison
                for image_name in image_names:
                    if normalize_name(image_name) == normalize_name(parsed_src_name):
                        print(f"Image correspondante trouvée : {image_name} (source: {src})")
                        if image_name not in image_positions or position < image_positions[image_name]:
                            image_positions[image_name] = position
                        break
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier '{file_path}': {e}")

# Vérifier tous les sous-dossiers et fichiers HTML
total_files = 0
for root, dirs, files in os.walk(site_folder):
    for file in files:
        if file.lower().endswith(('.html', '.htm')):  # Supporte les fichiers .html et .htm
            total_files += 1
            file_path = os.path.join(root, file)
            analyze_file(file_path, image_names)

# Trouver l'image la plus fréquemment trouvée en première position
if image_positions:
    most_common_image = min(image_positions, key=image_positions.get)
    print(f"Image la plus fréquemment trouvée en première position : {most_common_image}")
    
    # Ajouter l'image la plus fréquente dans le dossier de sortie
    for ext in ['.png', '.jpg', '.jpeg', '.gif', '.svg']:
        original_image_path = os.path.join(images_folder, most_common_image + ext)
        if os.path.exists(original_image_path):
            shutil.copy(original_image_path, output_folder)
            print(f"Image copiée : {original_image_path} vers {output_folder}")
            break

print(f"Total de fichiers analysés : {total_files}")