from PIL import Image, ImageDraw, ImageFont
import json
import os

# Dossiers de travail
json_folder = "./mnt/data"
icon_folder = "./icon_for_logo"
base_output_folder = "./website_downloaded"

# Trouver le dossier qui commence par "www."
website_folder = None
for folder in os.listdir(base_output_folder):
    if folder.startswith("www.") and os.path.isdir(os.path.join(base_output_folder, folder)):
        website_folder = folder
        break

if not website_folder:
    print("Erreur : Aucun dossier commençant par 'www.' n'a été trouvé dans le dossier de base.")
    exit()

# Créer le chemin de sortie
output_folder = os.path.join(base_output_folder, website_folder, "logo")

# Vérifier si le dossier de sortie existe, sinon le créer
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Parcourir chaque fichier JSON dans le dossier
for json_file in os.listdir(json_folder):
    if json_file.endswith('.json'):
        json_path = os.path.join(json_folder, json_file)
        
        # Charger les données JSON
        with open(json_path, 'r', encoding='utf-8') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                print(f"Erreur de décodage JSON dans le fichier: {json_file}")
                continue
            
            # Extraire les informations nécessaires
            shorted_name = None
            category = None
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, dict):
                        if item.get('type') == 'nom de société':
                            shorted_name = item.get('content')
                        elif item.get('type') == 'categorie':
                            category = item.get('content')
            
            # Continuer seulement si les informations sont présentes
            if not shorted_name or not category:
                continue
            
            # Trouver l'icône correspondant à la catégorie
            icon_path = os.path.join(icon_folder, f"{category.lower()}.png")
            if not os.path.exists(icon_path):
                print(f"Icône non trouvée pour la catégorie: {category}")
                continue
            
            # Charger l'icône et créer une nouvelle image pour le logo
            icon = Image.open(icon_path)
            icon = icon.resize((50, 50))  # Redimensionner l'icône pour qu'elle soit plus petite
            
            # Créer une nouvelle image avec une frame pour l'icône et le texte
            new_width = 400
            new_height = 100
            logo_image = Image.new('RGBA', (new_width, new_height), (255, 255, 255, 0))
            
            # Centrer verticalement l'icône et le texte
            icon_y_position = (new_height - icon.height) // 2
            logo_image.paste(icon, (10, icon_y_position), icon)
            
            # Ajouter le texte du nom abrégé à droite de l'icône
            draw = ImageDraw.Draw(logo_image)
            try:
                font = ImageFont.truetype("arialbd.ttf", 30)  # Police plus grande et épaisse
            except IOError:
                font = ImageFont.load_default()
            text_width, text_height = draw.textbbox((0, 0), shorted_name, font=font)[2:4]
            text_position = (70, (new_height - text_height) // 2)
            draw.text(text_position, shorted_name, fill="white", font=font)
            
            # Enregistrer l'image résultante
            output_path = os.path.join(output_folder, f"{shorted_name}_logo.png")
            logo_image.save(output_path)
            print(f"Logo généré pour {shorted_name}: {output_path}")
