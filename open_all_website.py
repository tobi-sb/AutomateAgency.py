import os
import webbrowser

# Chemin du dossier racine
base_directory = './website_save'

# Parcourir toutes les itérations dans le dossier racine
for iteration_folder in os.listdir(base_directory):
    iteration_path = os.path.join(base_directory, iteration_folder)
    # S'assurer qu'il s'agit bien d'un dossier
    if os.path.isdir(iteration_path):
        # Parcourir tous les sous-dossiers
        for sub_folder in os.listdir(iteration_path):
            # Chercher le dossier qui commence par 'www.'
            if sub_folder.startswith('www.'):
                sub_folder_path = os.path.join(iteration_path, sub_folder)
                index_file_path = os.path.join(sub_folder_path, 'index.html')
                # Si le fichier index.html existe, l'ouvrir dans le navigateur
                if os.path.isfile(index_file_path):
                    # Ouvrir le fichier index.html
                    webbrowser.get().open('file://' + os.path.abspath(index_file_path))
                    # Ouvrir le site web correspondant
                    webbrowser.get().open('https://' + sub_folder)