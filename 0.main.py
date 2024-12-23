import subprocess
import time
import sys
import os
import shutil

scripts = [
    '1_choose_city.py',
    '1.1_make_link.py',
    '2_blacklist.py',
    '2.1_blacklist.py',
    '3_sitemap.py',
    '4_text_scrap.py',
    '5_screenshot.py',
    '6_rank_website.py',
    '6.1_filter_rank_name.py',
    '7_doawload_website.py',    
    '7.3_nav-first-screen.py',
    '8_doawload_picture.py',
    '8.1_filter.py',
    '8.2_fav-icon-ban.py',
    '8.3_position_picture.py',
    '9_logo_generator.py',
    '9.1_edit_json.py',
    '9.2_update_logo.py',
    '9.9_nav-second-screen.py',
    '10_compare_image.py',
    '11_found_variante.py',
    '11.1_update_variante.py',
    '12_update_phone_email.py'
]

# Utilise l'environnement Python actuel pour exécuter les scripts
python_executable = sys.executable

# Fonction pour exécuter tous les scripts à partir d'un index donné
def run_scripts_from_index(start_index):
    for script in scripts[start_index:]:
        try:
            print(f"Exécution de {script}...")
            subprocess.run([python_executable, script], check=True)
            time.sleep(1)  # Délai de 1 seconde entre chaque script
        except subprocess.CalledProcessError as e:
            print(f"Erreur lors de l'exécution de {script}: {e}")
        except FileNotFoundError:
            print(f"Le script {script} est introuvable.")

# Boucle principale pour exécuter les scripts 3 fois
for i in range(3):
    print(f"\nItération {i + 1} sur 3:")

    if i == 0:
        run_scripts_from_index(0)  # Exécuter tous les scripts lors de la première itération
    else:
        run_scripts_from_index(9)  # Reprendre à partir de '7_doawload_website.py' pour les itérations suivantes

    # Copier le dossier ./website_downloaded dans ./website_save
    website_downloaded_dir = './website_downloaded'
    website_save_dir = './website_save'
    if os.path.exists(website_downloaded_dir):
        if not os.path.exists(website_save_dir):
            os.makedirs(website_save_dir)
        shutil.copytree(website_downloaded_dir, os.path.join(website_save_dir, f'iteration_{i + 1}'), dirs_exist_ok=True)
        print(f"{website_downloaded_dir} copié dans {website_save_dir} (itération {i + 1}).")
    else:
        print(f"Le dossier {website_downloaded_dir} est introuvable.")

    # Supprimer la première ligne du fichier ./final_website_rank.txt
    rank_file_path = './final_website_rank.txt'
    if os.path.exists(rank_file_path):
        with open(rank_file_path, 'r') as file:
            lines = file.readlines()
        with open(rank_file_path, 'w') as file:
            file.writelines(lines[1:])
        print(f"Première ligne de {rank_file_path} supprimée.")
    else:
        print(f"Le fichier {rank_file_path} est introuvable.")

print("Tous les scripts ont été exécutés.")
