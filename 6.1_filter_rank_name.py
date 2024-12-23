import re

# Fonction pour ajouter www. si besoin
def ajouter_www(url):
    # Remplacer "___" par "://"
    url = url.replace("___", "://")

    # Vérifie si l'URL commence par "http://" ou "https://" (et ajoute "https://" si ce n'est pas le cas)
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    # Si "www." n'est pas présent, l'ajouter après "https://"
    if not re.match(r"https?://www\.", url):
        url = re.sub(r"https?://", "https://www.", url)
    
    return url

# Lecture du fichier et mise à jour des URLs
with open('./final_website_rank.txt', 'r') as fichier:
    urls = fichier.readlines()

urls_mises_a_jour = [ajouter_www(url.strip()) + "\n" for url in urls]

# Écriture du fichier avec les URLs mises à jour
with open('./final_website_rank.txt', 'w') as fichier:
    fichier.writelines(urls_mises_a_jour)

print("Mise à jour des URLs terminée.")