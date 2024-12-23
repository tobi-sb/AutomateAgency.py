import os
import re

# Paths definition
html_directory = './website_downloaded'
variant_file_path = './variante.txt'
logo_directory = ''
logo_name = ''

# Find the www directory and logo image path
for root, dirs, files in os.walk(html_directory):
    for dir_name in dirs:
        if dir_name.startswith('www.'):
            logo_directory = os.path.join(root, dir_name, 'logo')
            if os.path.exists(logo_directory):
                for file_name in os.listdir(logo_directory):
                    if file_name.endswith(('.png', '.jpg', '.jpeg', '.svg', '.gif')):
                        logo_name = file_name
                        break
            break

if not logo_directory or not logo_name:
    raise FileNotFoundError("Logo directory or logo file not found.")

# Load variant image names from variante.txt
with open(variant_file_path, 'r') as f:
    variant_images = [line.strip() for line in f.readlines()]

# Define new logo source
new_logo_source = f'./logo/{logo_name}'

# Traverse through all HTML files and replace image sources
for root, _, files in os.walk(html_directory):
    for file_name in files:
        if file_name.endswith('.html'):
            html_file_path = os.path.join(root, file_name)
            try:
                with open(html_file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except UnicodeDecodeError:
                with open(html_file_path, 'r', encoding='latin-1') as f:
                    content = f.read()
            
            # Replace all variant image sources with the new logo source
            for variant_image in variant_images:
                if re.search(rf'src\s*=\s*["\'].*{re.escape(variant_image)}["\']', content):
                    print(f'Updating image source in file: {html_file_path}, replacing: {variant_image} with: {new_logo_source}')
                content = re.sub(rf'src\s*=\s*["\'].*{re.escape(variant_image)}["\']', f'src="{new_logo_source}"', content)
            
            # Write the updated content back to the HTML file
            with open(html_file_path, 'w', encoding='utf-8') as f:
                f.write(content)

print("Image sources updated successfully.")
