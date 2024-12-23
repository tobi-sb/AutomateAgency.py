import os
import logging
from urllib.parse import urlparse

# Configurer les logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Fonction pour charger la liste noire depuis un fichier
def load_blacklist(file_path):
    if not os.path.exists(file_path):
        logging.error(f"Le fichier {file_path} n'existe pas.")
        return []
    with open(file_path, 'r', encoding='utf-8') as f:
        return [line.strip().lower() for line in f.readlines()]

# Charger la liste noire depuis le fichier
BLACKLIST_FILE_PATH = './blacklist.txt'
BLACKLIST = load_blacklist(BLACKLIST_FILE_PATH)

# Fonction pour charger les liens depuis un fichier
def get_links(file_path):
    if not os.path.exists(file_path):
        logging.error(f"Le fichier {file_path} n'existe pas.")
        return []
    with open(file_path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f.readlines()]

# Fonction pour sauvegarder les liens filtrés dans un fichier
def save_links(file_path, links):
    with open(file_path, 'w', encoding='utf-8') as f:
        for link in links:
            f.write(link + '\n')
    logging.info(f"Enregistré {len(links)} liens dans {file_path}")

# Fonction pour obtenir l'URL de base avec le schéma
def get_base_url_with_scheme(url):
    parsed_url = urlparse(url)
    return f"{parsed_url.scheme}://{parsed_url.netloc}".lower()

# Fonction principale pour filtrer les liens
if __name__ == "__main__":
    LINK_FILE_PATH = './link.txt'
    FINAL_LINK_PATH = './final_link.txt'

    # Charger les liens depuis le fichier link.txt
    links = get_links(LINK_FILE_PATH)
    logging.info(f"Nombre de liens chargés depuis {LINK_FILE_PATH}: {len(links)}")

    if not links:
        logging.error("Aucun lien n'a été chargé. Vérifiez le fichier d'entrée.")

    # Filtrer les liens en utilisant la liste noire (en comparant les domaines exacts et sous-domaines)
    filtered_links = []
    for link in links:
        link = link.strip()
        parsed_url = urlparse(link)
        domain = parsed_url.netloc.lower()

        # Vérification stricte avec la liste noire pour le domaine et les sous-domaines
        blacklisted = False
        for blacklisted_site in BLACKLIST:
            if domain == blacklisted_site or domain.endswith(f".{blacklisted_site}"):
                logging.info(f"Lien supprimé car en liste noire: {link} (domaine : {domain})")
                blacklisted = True
                break

        if not blacklisted:
            filtered_links.append(get_base_url_with_scheme(link))

    logging.info(f"Nombre de liens après filtrage de la liste noire: {len(filtered_links)}")

    # Supprimer les doublons et trier les liens
    unique_links = sorted(set(filtered_links))
    logging.info(f"Nombre de liens uniques après suppression des doublons: {len(unique_links)}")

    # Sauvegarder les liens uniques dans final_link.txt
    save_links(FINAL_LINK_PATH, unique_links)
    logging.info(f"Liens uniques sauvegardés dans {FINAL_LINK_PATH}")
