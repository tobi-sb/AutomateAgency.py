import os
import re
import json
from bs4 import BeautifulSoup
from pathlib import Path

# Charger les informations du fichier JSON
with open('./mnt/data/company_1.json', 'r', encoding='utf-8') as json_file:
    company_data = json.load(json_file)
    new_phone = None
    new_email = None
    for item in company_data:
        if item.get("type") == "numéro de téléphone":
            new_phone = item.get("content")
        elif item.get("type") == "email":
            new_email = item.get("content")

# Dossier contenant le site web téléchargé
website_dir = './website_downloaded'
backup_file = './mnt/data/backup_contacts.json'

# Expressions régulières pour les numéros de téléphone et les adresses e-mail
phone_pattern = re.compile(r'\b\d{2}(?:[ \-]?\d{2}){4}\b|\b\d{10}\b')
email_pattern = re.compile(r'\b[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+\b')

# Fonction pour remplacer les numéros de téléphone et les e-mails dans le contenu
def replace_contact_details(soup, new_phone, new_email, backup_data):
    text_elements = soup.find_all(string=phone_pattern) + soup.find_all(string=email_pattern)
    
    for element in text_elements:
        # Sauvegarder le texte original
        original_text = element.strip()
        
        # Remplacer les numéros de téléphone
        if phone_pattern.search(original_text) and new_phone:
            backup_data['phones'].append(original_text)
            new_text = phone_pattern.sub(new_phone, original_text)
            element.replace_with(new_text)
            print(f"Numéro de téléphone remplacé par: {new_phone}")
        
        # Remplacer les adresses e-mail
        if email_pattern.search(original_text) and new_email:
            backup_data['emails'].append(original_text)
            new_text = email_pattern.sub(new_email, original_text)
            element.replace_with(new_text)
            print(f"Adresse e-mail remplacée par: {new_email}")

# Initialiser les données de sauvegarde
backup_data = {'phones': [], 'emails': []}

# Parcourir les fichiers HTML du site web
for root, _, files in os.walk(website_dir):
    for file in files:
        if file.endswith('.html'):
            file_path = Path(root) / file
            print(f"Analyse du fichier: {file_path}")
            
            # Lire le contenu du fichier HTML
            with open(file_path, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f, 'html.parser')
            
            # Remplacer les coordonnées par celles du fichier JSON
            replace_contact_details(soup, new_phone, new_email, backup_data)
            
            # Écrire les modifications dans le fichier HTML
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(str(soup))

# Sauvegarder les données de backup dans un fichier JSON
with open(backup_file, 'w', encoding='utf-8') as backup_json:
    json.dump(backup_data, backup_json, ensure_ascii=False, indent=4)

print("Remplacement des numéros de téléphone et des e-mails terminé.")
