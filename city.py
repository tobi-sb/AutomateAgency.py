# Script pour extraire uniquement la troisième colonne

# Chemins des fichiers d'entrée et de sortie
input_file = './FR_unique copy.txt'
output_file = './FR_unique_filtered.txt'

# Ouverture du fichier d'entrée et traitement ligne par ligne
with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
    for line in infile:
        # Séparation de la ligne par des tabulations et extraction de la troisième colonne
        columns = line.split('\t')
        if len(columns) > 2:
            # Écriture de la troisième colonne dans le fichier de sortie
            outfile.write(columns[2] + '\n')

print(f"Les noms des villes ont été extraits dans le fichier : {output_file}")
