import os
from bs4 import BeautifulSoup

# Chemins vers les dossiers
website_folder = './website_downloaded'
images_folder = './images_filter1'

# Extensions communes pour les fav-icons
favicon_extensions = ['.ico', '.png', '.svg', '.jpg', '.jpeg']

# Rechercher la balise fav-icon dans un fichier HTML
def find_favicon_in_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    favicons = []
    # Rechercher les balises <link> avec rel="icon" ou rel="shortcut icon"
    for link in soup.find_all('link', rel=lambda x: x and 'icon' in x):
        href = link.get('href')
        if href and any(href.lower().endswith(ext) for ext in favicon_extensions):
            favicons.append(href)
    return favicons

# Parcours des fichiers HTML dans le dossier et recherche des fav-icons
def process_html_files():
    for root, dirs, files in os.walk(website_folder):
        for filename in files:
            if filename.endswith('.html'):
                file_path = os.path.join(root, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as html_file:
                        html_content = html_file.read()
                except UnicodeDecodeError:
                    # Si la lecture échoue avec utf-8, essayez d'autres encodages courants
                    try:
                        with open(file_path, 'r', encoding='latin-1') as html_file:
                            html_content = html_file.read()
                    except UnicodeDecodeError:
                        print(f"Impossible de lire le fichier {file_path} avec les encodages courants.")
                        continue

                favicons = find_favicon_in_html(html_content)
                for favicon in favicons:
                    favicon_path = os.path.join(images_folder, os.path.basename(favicon))
                    if os.path.exists(favicon_path):
                        print(f"Suppression du fichier fav-icon : {favicon_path}")
                        os.remove(favicon_path)

if __name__ == '__main__':
    process_html_files()
