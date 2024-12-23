import subprocess
import os
import shutil

# Chemin vers le fichier WebCopy
wcopy_path = r'C:\Program Files\Cyotek\WebCopy\wcopy.exe'

# Chemin vers le fichier contenant l'URL
file_path = './final_website_rank.txt'

# Chemin vers le dossier de sortie principal
output_base_folder = './website_downloaded'

# Vider le dossier ./website_downloaded avant de commencer
if os.path.exists(output_base_folder):
    shutil.rmtree(output_base_folder)
os.makedirs(output_base_folder, exist_ok=True)

# Lire la première URL du fichier
with open(file_path, 'r') as file:
    first_url = file.readline().strip()

# Vérifier si l'URL est valide
if first_url:
    # Définir le dossier de sortie pour le site spécifique
    output_folder = os.path.join(output_base_folder, 'www.website.com')

    # Supprimer le dossier de sortie s'il existe déjà
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    os.makedirs(output_folder, exist_ok=True)

    # Construire la commande pour utiliser Cyotek WebCopy
    command = [
        wcopy_path,
        first_url,
        '/o', os.path.abspath(output_folder),
        '/recursive',
        '/empty'  # Vide le dossier de sortie avant le téléchargement
    ]

    # Exécuter la commande
    try:
        subprocess.run(command, check=True)
        print(f'Téléchargement de {first_url} terminé avec succès.')

        # Vérifier le nombre de fichiers et d'images dans le dossier
        num_files = sum(len(files) for _, _, files in os.walk(output_folder))
        num_images = sum(1 for _, _, files in os.walk(output_folder) for file in files if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')))

        # Condition d'échec
        if num_files < 9 or num_images < 5:
            print("Le téléchargement est considéré comme un échec en raison du nombre insuffisant de fichiers ou d'images.")

            # Supprimer l'URL du fichier
            with open(file_path, 'r') as file:
                lines = file.readlines()
            with open(file_path, 'w') as file:
                for line in lines:
                    if line.strip() != first_url:
                        file.write(line)

            # Lancer le script 7_download_website.py
            download_script = './7_doawload_website.py'
            try:
                subprocess.run(['python', download_script], check=True)
            except subprocess.CalledProcessError as e:
                print(f'Erreur lors de l\'exécution du script de téléchargement : {e}')
        else:
            print("Téléchargement réussi avec suffisamment de fichiers et d'images.")

        # Renommer les fichiers .htm en .html
        for dirpath, _, filenames in os.walk(output_folder):
            for filename in filenames:
                if filename.lower().endswith('.htm'):
                    old_path = os.path.join(dirpath, filename)
                    new_path = os.path.join(dirpath, filename + 'l')  # Ajoute 'l' pour devenir .html
                    os.rename(old_path, new_path)
    except subprocess.CalledProcessError as e:
        print(f'Erreur lors du téléchargement du site : {e}')
else:
    print('Aucune URL trouvée dans le fichier.')
