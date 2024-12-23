# Fonction pour traiter et détecter les doublons basés sur le troisième mot
def remove_duplicates_by_third_word(file_path, output_path):
    # Ouvrir et lire le fichier ligne par ligne
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Dictionnaire pour stocker les lignes par troisième mot
    unique_lines = {}
    
    # Parcourir chaque ligne
    for line in lines:
        # Séparer les mots en utilisant l'espace comme séparateur
        words = line.split()
        
        # Vérifier qu'il y a au moins 3 mots
        if len(words) >= 3:
            third_word = words[2]
            
            # Si ce troisième mot n'a pas encore été rencontré, on garde la ligne
            if third_word not in unique_lines:
                unique_lines[third_word] = line

    # Écrire les lignes uniques dans le fichier de sortie
    with open(output_path, 'w', encoding='utf-8') as output_file:
        for line in unique_lines.values():
            output_file.write(line)

    print(f"Le fichier sans doublons a été créé: {output_path}")

# Exécution de la fonction
file_path = './FR.txt'  # Le fichier d'entrée
output_path = './FR_unique.txt'  # Le fichier de sortie
remove_duplicates_by_third_word(file_path, output_path)
