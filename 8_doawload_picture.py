import os
import shutil

# Dossier de la page Web cible
dossier_cible = "./website_downloaded"

# Nom du dossier pour enregistrer les images
dossier_images = "images"

# Créer le dossier s'il n'existe pas encore
if not os.path.exists(dossier_images):
    os.makedirs(dossier_images)
else:
    # Supprimer toutes les images du dossier existant
    for fichier in os.listdir(dossier_images):
        chemin_fichier = os.path.join(dossier_images, fichier)
        if os.path.isfile(chemin_fichier):
            os.remove(chemin_fichier)

# Fonction pour copier une image
def copier_image(chemin_source, chemin_destination):
    try:
        with open(chemin_source, 'rb') as fichier_source:
            with open(chemin_destination, 'wb') as fichier_destination:
                fichier_destination.write(fichier_source.read())
        print(f"Image copiée : {chemin_destination}")
    except Exception as e:
        print(f"Exception lors de la copie de {chemin_source} : {e}")

# Parcourir les fichiers du dossier cible
for root, dirs, files in os.walk(dossier_cible):
    for fichier in files:
        if fichier.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.svg')):
            chemin_source = os.path.join(root, fichier)
            chemin_destination = os.path.join(dossier_images, fichier)
            copier_image(chemin_source, chemin_destination)