import os
import re
import requests
from bs4 import BeautifulSoup
from collections import defaultdict

# Chemin du fichier contenant les liens
links_file = "filtered_list.txt"
# Dossier où le contenu sera enregistré
output_directory = "./website_content"
# Fichier pour les liens valides
valid_links_file = "filtered_list.txt"

# Supprimer tous les fichiers dans le dossier de destination s'il existe déjà
if os.path.exists(output_directory):
    for filename in os.listdir(output_directory):
        file_path = os.path.join(output_directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                os.rmdir(file_path)
        except Exception as e:
            print(f"Erreur lors de la suppression de {file_path}: {e}")

# Créer le dossier de destination s'il n'existe pas déjà
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Lire le fichier link.txt
with open(links_file, "r") as file:
    links = [link.strip() for link in file.readlines()]

# Définir l'User-Agent pour contourner les erreurs 403
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
}

# Fonction pour raccourcir les liens
def shorten_link(link):
    match = re.match(r'(https?://[^/]+)', link)
    return match.group(1) if match else link


# Fonction pour nettoyer le texte et compter les mots
def clean_and_count_text(text):
    text = text.strip()
    text = re.sub(r'\s{3,}', '  ', text)
    cleaned_lines = [line.strip() for line in text.splitlines() if line.strip()]
    unified_text = " ".join(cleaned_lines)

    word_frequency = defaultdict(int)
    words = unified_text.split()
    for word in words:
        word_frequency[word] += 1

    cleaned_text_with_counts = []
    for word, count in word_frequency.items():
        if count > 1:
            cleaned_text_with_counts.append(f"{word} ({count})")
        else:
            cleaned_text_with_counts.append(word)

    return " ".join(cleaned_text_with_counts)

# Fonction pour extraire tout le texte pertinent d'un site web
def extract_full_text(soup):
    full_text = soup.get_text(separator="\n")

    meta_texts = [meta.get("content") for meta in soup.find_all("meta", content=True)]
    meta_text = "\n".join([text for text in meta_texts if text])

    alt_texts = [img.get("alt") for img in soup.find_all("img", alt=True)]
    alt_text = "\n".join([text for text in alt_texts if text])

    link_titles = [link.get("title") for link in soup.find_all("a", title=True)]
    link_text = "\n".join([text for text in link_titles if text])

    combined_text = "\n".join([full_text, meta_text, alt_text, link_text])

    return combined_text

# Initialiser un compteur de succès pour nommer correctement les fichiers
success_count = 0
# Stocker les liens téléchargés avec succès
successful_links = []

# Parcourir chaque lien du fichier
for index, link in enumerate(links):
    if not link:
        continue

    try:
        response = requests.get(link, headers=headers, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")
        page_text = extract_full_text(soup)

        cleaned_text = clean_and_count_text(page_text)

        # Nettoyer l'URL pour créer un nom de fichier valide
        base_file_name = re.sub(r'[\\/*?:"<>|#]', "_", link)

        # Incrémenter le compteur de succès et utiliser pour le nom du fichier
        success_count += 1
        numbered_file_name = f"{success_count}_{base_file_name}.txt"
        file_path = os.path.join(output_directory, numbered_file_name)

        with open(file_path, "w", encoding="utf-8") as text_file:
            text_file.write(cleaned_text)

        print(f"[{success_count}/{len(links)}] Enregistré : {file_path}")

        # Ajouter le lien à la liste des succès
        successful_links.append(shorten_link(link))

    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de l'accès à {link}: {e}")
    except Exception as e:
        print(f"Erreur lors du traitement de {link}: {e}")

# Écrire les liens valides dans le fichier final_link.txt
with open(valid_links_file, "w") as file:
    for link in successful_links:
        file.write(link + "\n")

print(f"Scraping terminé. {len(successful_links)}/{len(links)} liens enregistrés avec succès.")
print(f"Les liens valides ont été enregistrés dans le fichier : {valid_links_file}")