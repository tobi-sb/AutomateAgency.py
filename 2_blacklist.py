def simplify_url(url):
    return url.replace("https://www.", "")

# Lire les liens du fichier 6.2_blacklist.txt
with open("./6.2_blacklist.txt", "r") as f:
    urls = f.readlines()

# Simplifier les URLs en supprimant 'https://www.'
simplified_urls = [simplify_url(url.strip()) for url in urls]

# Ajouter les liens simplifiés au fichier blacklist.txt
with open("./blacklist.txt", "a") as f:
    for url in simplified_urls:
        if url:  # Éviter d'écrire des lignes vides
            f.write(url + "\n")

# Vider le fichier 6.2_blacklist.txt
with open("./6.2_blacklist.txt", "w") as f:
    f.truncate(0)

print("Mise à jour du fichier blacklist.txt terminée, et suppression du contenu de 6.2_blacklist.txt.")
