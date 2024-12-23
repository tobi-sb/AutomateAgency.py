from PIL import Image
import imagehash
import os
import cairosvg

# Dossiers
logo_folder = './images_filter2'
images_folder = './images'

# Fonction pour charger une image, convertir les SVG si nécessaire
def load_image(image_path):
    if image_path.lower().endswith('.svg'):
        png_path = image_path + '.png'
        cairosvg.svg2png(url=image_path, write_to=png_path)
        return Image.open(png_path)
    else:
        return Image.open(image_path)

# Charger le logo à comparer
logo_path = os.path.join(logo_folder, os.listdir(logo_folder)[0])
logo_image = load_image(logo_path)
logo_hash = imagehash.average_hash(logo_image)

# Parcourir toutes les images dans ./images et comparer avec le logo
matching_images = []
for image_name in os.listdir(images_folder):
    image_path = os.path.join(images_folder, image_name)
    try:
        current_image = load_image(image_path)
        current_hash = imagehash.average_hash(current_image)
        
        # Comparer les hachages (une différence de 0 signifie que les images sont identiques)
        if logo_hash - current_hash < 5:  # Le seuil peut être ajusté selon la tolérance souhaitée
            matching_images.append(image_name)
    except Exception as e:
        print(f"Erreur lors de l'ouverture de l'image {image_name}: {e}")

# Afficher les images correspondantes
if matching_images:
    print("Images correspondantes trouvées :")
    for match in matching_images:
        print(match)
else:
    print("Aucune image correspondante trouvée.")