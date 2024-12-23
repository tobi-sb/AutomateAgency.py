from PIL import Image, ImageChops
import imagehash
import os
import cairosvg

# Dossiers
logo_folder = './images_filter2'
images_folder = './images'
variante_file = './variante.txt'

# Fonction pour charger une image, convertir les SVG si nécessaire
def load_image(image_path):
    print(f"Chargement de l'image : {image_path}")
    if image_path.lower().endswith('.svg'):
        png_path = image_path + '.png'
        print(f"Conversion de SVG en PNG : {png_path}")
        cairosvg.svg2png(url=image_path, write_to=png_path)
        image = Image.open(png_path)
    else:
        image = Image.open(image_path)
    
    # Vérifier si l'image est en mode 'P' et la convertir en 'RGBA'
    if image.mode == 'P':
        print(f"Conversion de l'image en mode 'RGBA' : {image_path}")
        image = image.convert('RGBA')
    
    return image

# Fonction pour enlever toutes les marges transparentes d'une image
def trim(image):
    print("Suppression des marges transparentes de l'image")
    bg = Image.new(image.mode, image.size, image.getpixel((0, 0)))
    diff = ImageChops.difference(image, bg)
    bbox = diff.getbbox()
    if bbox:
        return image.crop(bbox)
    return image

# Charger le logo à comparer
logo_path = os.path.join(logo_folder, os.listdir(logo_folder)[0])
print(f"Chargement du logo : {logo_path}")
logo_image = load_image(logo_path)
logo_image = trim(logo_image)
logo_hash = imagehash.whash(logo_image, hash_size=16)  # Utiliser whash pour une meilleure tolérance
print(f"Hachage du logo : {logo_hash}")

# Parcourir toutes les images dans ./images, enlever les marges et comparer avec le logo
matching_images = []
for image_name in os.listdir(images_folder):
    image_path = os.path.join(images_folder, image_name)
    print(f"\nTraitement de l'image : {image_name}")
    try:
        current_image = load_image(image_path)
        current_image = trim(current_image)  # Supprimer toutes les marges de l'image
        current_hash = imagehash.whash(current_image, hash_size=16)
        print(f"Hachage de l'image courante : {current_hash}")
        
        # Comparer les hachages (une différence de 0 signifie que les images sont identiques)
        hash_difference = logo_hash - current_hash
        print(f"Différence de hachage : {hash_difference}")
        if hash_difference < 10:  # Augmenter le seuil pour plus de tolérance
            print(f"Image correspondante trouvée : {image_name}")
            matching_images.append(image_name)
        else:
            print(f"Image non correspondante : {image_name}")
    except Exception as e:
        print(f"Erreur lors de l'ouverture de l'image {image_name}: {e}")

# Écrire les images correspondantes dans variante.txt
print("\nÉcriture des résultats dans le fichier variante.txt")
with open(variante_file, 'w') as f:
    if matching_images:
        for match in matching_images:
            f.write(match + '\n')
            print(f"Image correspondante écrite : {match}")
    else:
        f.write("Aucune image correspondante trouvée.")
        print("Aucune image correspondante trouvée.")