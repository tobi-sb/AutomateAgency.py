import os
import subprocess
from PIL import Image, ImageChops, ImageStat
import time
import sys
import importlib

def compare_images(image1_path, image2_path, threshold=1):
    img1 = Image.open(image1_path).convert('RGB')
    img2 = Image.open(image2_path).convert('RGB')
    diff = ImageChops.difference(img1, img2)
    # Vérifier si la différence contient des pixels non nuls
    bbox = diff.getbbox()
    if bbox is None:
        return True
    # Calculer la moyenne des différences de pixels
    stat = ImageStat.Stat(diff)
    diff_mean = sum(stat.mean) / len(stat.mean)
    return diff_mean <= threshold

def ensure_package_installed(package_name):
    try:
        importlib.import_module(package_name)
    except ImportError:
        print(f"Package '{package_name}' not found. Installing...")
        subprocess.check_call(['./env/Scripts/python.exe', '-m', 'pip', 'install', package_name])

# Fonction principale pour comparer les images et exécuter les scripts
def main():
    # Chemins des images
    before_mobile_path = './website_downloaded/img_before_after_nav/nav-screen-before-mobile.png'
    after_mobile_path = './website_downloaded/img_before_after_nav/nav-screen-mobile.png'

    before_pc_path = './website_downloaded/img_before_after_nav/nav-screen-before-pc.png'
    after_pc_path = './website_downloaded/img_before_after_nav/nav-screen-pc.png'

    # Comparaison des deux groupes d'images
    mobile_images_identical = compare_images(before_mobile_path, after_mobile_path)
    pc_images_identical = compare_images(before_pc_path, after_pc_path)

    # Si les deux comparaisons sont identiques, effectuer la suppression
    if mobile_images_identical and pc_images_identical:
        print('Both mobile and PC images are identical')

        # Suppression des images dans les dossiers
        images_filter2_path = './images_filter2'
        images_filter1_path = './images_filter1'

        images_in_filter2 = [f for f in os.listdir(images_filter2_path) if os.path.isfile(os.path.join(images_filter2_path, f))]

        if len(images_in_filter2) == 1:
            image_name = images_in_filter2[0]

            image_path_in_filter1 = os.path.join(images_filter1_path, image_name)
            image_path_in_filter2 = os.path.join(images_filter2_path, image_name)

            if os.path.exists(image_path_in_filter1):
                os.remove(image_path_in_filter1)
                print(f"Deleted {image_name} from {images_filter1_path}")

            os.remove(image_path_in_filter2)
            print(f"Deleted {image_name} from {images_filter2_path}")
        else:
            print("Either no image or more than one image found in ./images_filter2")
            # Supprimer la première ligne de ./final_website_rank.txt
            with open('./final_website_rank.txt', 'r') as file:
                lines = file.readlines()
            with open('./final_website_rank.txt', 'w') as file:
                file.writelines(lines[1:])
            # Lancer le script ./10.1_if_fail.py
            print("Executing ./10.1_if_fail.py...")
            subprocess.run(['./env/Scripts/python.exe', './10.1_if_fail.py'], check=True)
            return

        # Exécution des scripts supplémentaires
        scripts_to_run = [
            './8.3_position_picture.py',
            './9.3_logo_backup.py',
            './9.2_update_logo.py',
            './9.9_nav-second-screen.py'
        ]

        for script in scripts_to_run:
            try:
                if script == './9.9_nav-second-screen.py':
                    ensure_package_installed('selenium')

                print(f"Executing {script}...")
                subprocess.run(['./env/Scripts/python.exe', script], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                print(f"Successfully executed {script}")
                time.sleep(2)  # Attendre 2 secondes entre chaque exécution de script
            except subprocess.CalledProcessError as e:
                print(f"Error while executing {script}: {e.stderr}")

        # Relancer l'analyse des images après l'exécution des scripts
        main()
    else:
        print('One or both image comparisons are different')

if __name__ == "__main__":
    main()
