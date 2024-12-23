# Script pour supprimer les lignes dupliquées dans ./client_src

def remove_duplicates(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    # Supprimer les doublons tout en conservant l'ordre
    unique_lines = list(dict.fromkeys(lines))
    with open(file_path, 'w') as file:
        file.writelines(unique_lines)

if __name__ == "__main__":
    remove_duplicates('./client_src.txt')
