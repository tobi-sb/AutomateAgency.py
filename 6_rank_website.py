import os
import openai
import json
import re

# Load the JSON file containing the client information
with open('./mnt/data/company_1.json', 'r', encoding='utf-8') as json_file:
    client_info = json.load(json_file)

# Extract the category from the JSON file
client_category = next((item['content'] for item in client_info if item['type'] == 'categorie'), None)

# Set up the OpenAI API key
openai.api_key = ""

total_tokens_used = 0
website_scores = []

def get_text_analysis_score(text, client_category):
    global total_tokens_used
    messages = [
        {"role": "system", "content": "You are an expert in matching companies to client needs."},
        {"role": "user", "content": f"The client category is '{client_category}'. Please read the following website content and provide a score between 0 and 100 based on how well the content matches the client's category. Only provide the numerical score:\n\n{text}"}
    ]
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=10
    )
    total_tokens_used += response['usage']['total_tokens']
    score = response.choices[0].message['content'].strip()
    try:
        return float(score)
    except ValueError:
        print(f"Erreur de conversion du score: {score}")
        return 0.0

def get_design_analysis_score(description):
    global total_tokens_used
    messages = [
        {"role": "system", "content": "You are a highly critical web design expert. Pay attention to the details, and penalize poor design choices such as bad color schemes, poor typography, cluttered layout, and unbalanced elements."},
        {"role": "user", "content": f"Based on the following website design description, evaluate how visually appealing and attractive the design is. Provide a score between 0 and 100 for the overall attractiveness of the design. Be very strict in your evaluation. Only provide the numerical score:\n\n{description}. Elements to consider include: \n1. **Color Usage**: Are the colors complementary, visually pleasing, or do they clash? Are they used consistently across the site?\n2. **Typography**: Is the font readable, appropriate for the target audience, and consistent? Does it align with the website's overall style and brand identity?\n3. **Layout**: Is the page layout clean, well-organized, and easy to navigate? Does the layout create a balanced visual flow?\n4. **Image Quality**: Are the images high quality, well-integrated, and contextually appropriate? Do they support the website's message?\n5. **Overall Aesthetic**: Does the design look modern and professional? Is it consistent with the website's purpose? Does it use modern design trends effectively?\n6. **Performance and Responsiveness**: Does the website load quickly? Is it responsive across different devices, including mobile, tablet, and desktop?\n7. **Accessibility**: Are elements accessible to all users, including those with disabilities (e.g., sufficient contrast for readability, descriptive alt texts for images)?\n8. **User Experience Standards**: Does the design follow modern UX/UI standards, such as easy navigation, clear call-to-actions, and user-friendly interactions?\n9. **Modernity**: Does the website use modern design elements (e.g., flat design, modern typography, animations, micro-interactions) effectively to create a fresh and current look?\n\nPenalize for issues like clashing colors, illegible text, excessive clutter, inconsistent branding, poor visual balance, slow performance, or lack of responsiveness. Provide examples of both good and bad design to justify your scoring."}
    ]
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=10
    )
    total_tokens_used += response['usage']['total_tokens']
    score = response.choices[0].message['content'].strip()
    try:
        return float(score)
    except ValueError:
        print(f"Erreur de conversion du score: {score}")
        return 0.0

def generate_design_description(screenshot_paths):
    description = ""
    for path in screenshot_paths:
        version = path.split(os.sep)[-2]
        description += f"Screenshot from the {version} version: This version of the website includes elements like a color scheme that should be visually appealing and consistent, a layout that is well-organized, typography that is readable, and overall spacing that provides a balanced look. It also features appropriate image usage that supports the content, ensuring that all visual elements align with modern design standards and are suitable for the target audience. "
    return description

# Clear the ./rank_result folder
if os.path.exists('./rank_result'):
    for file in os.listdir('./rank_result'):
        if file.endswith('.json'):
            os.remove(os.path.join('./rank_result', file))

# Iterate over each website in the ./website_content folder
print("Début du script...")
for filename in os.listdir('./website_content'):
    if filename.endswith('.txt'):
        try:
            print(f"Fichier analysé : {filename}")
            website_id = filename.split('_')[0]
            website_name = '_'.join(filename.split('_')[1:]).replace('.txt', '')
            print(f"Website ID: {website_id}, Website Name: {website_name}")
            
            # Load the text content of the website
            with open(f'./website_content/{filename}', 'r', encoding='utf-8') as txt_file:
                website_text = txt_file.read()
            
            # Replace http URLs with https URLs
            website_text = re.sub(r'http://', 'https://', website_text)
            
            # Get the text analysis score
            text_score = get_text_analysis_score(website_text, client_category)
            print(f"Text Analysis Score: {text_score}")
            
            # Locate the corresponding screenshot folder by matching the identifier
            screenshot_folder = None
            for folder in os.listdir('./screenshots'):
                if re.match(f'^{website_id}_', folder):
                    screenshot_folder = os.path.join('./screenshots', folder)
                    break
            
            screenshot_paths = []
            if screenshot_folder and os.path.exists(screenshot_folder):
                for subfolder in ['Laptop', 'PC', 'Tablette', 'Phone']:
                    subfolder_path = os.path.join(screenshot_folder, subfolder)
                    if os.path.exists(subfolder_path):
                        for f in os.listdir(subfolder_path):
                            if f.endswith('.png'):
                                screenshot_paths.append(os.path.join(subfolder_path, f))
            else:
                print(f"Aucun dossier de capture d'écran trouvé pour {website_name}.")
            
            if screenshot_paths:
                # Generate design description for screenshots
                design_description = generate_design_description(screenshot_paths)
                # Get the design analysis score
                design_score = get_design_analysis_score(design_description)
                print(f"Design Analysis Score: {design_score}")
            else:
                design_score = None
                print(f"Aucune capture d'écran trouvée dans les sous-dossiers pour {website_name}.")
            
            # Calculate the average score if both scores are available, with a weight of 1.5 for design and 1 for text
            if design_score is not None:
                average_score = (text_score + 1.5 * design_score) / 2.5
                website_scores.append((website_name, average_score))
                print(f"Average Score: {average_score}")
            else:
                average_score = None
            
            # Create a JSON file with the results in the ./rank_result folder
            result_data = {
                "website_name": website_name,
                "text_score": text_score,
                "design_score": design_score,
                "average_score": average_score
            }
            if not os.path.exists('./rank_result'):
                os.makedirs('./rank_result')
            with open(f'./rank_result/{website_name}.json', 'w', encoding='utf-8') as result_file:
                json.dump(result_data, result_file, ensure_ascii=False, indent=4)
            
            print(f"Résultats sauvegardés dans ./rank_result/{website_name}.json")
            print("---------------------------------------")
        except Exception as e:
            print(f"Erreur lors de l'analyse de {filename}: {e}")

# Print the total token usage
print(f"Total tokens used: {total_tokens_used}")

# Print the top 5 websites by average score
top_5_websites = sorted(website_scores, key=lambda x: x[1], reverse=True)[:5]
print("Top 5 Websites by Average Score:")
for rank, (website, score) in enumerate(top_5_websites, start=1):
    print(f"{rank}. {website} - Average Score: {score}")

# Write the top 10 websites by average score to ./final_website_rank.txt
top_10_websites = sorted(website_scores, key=lambda x: x[1], reverse=True)[:10]
with open('./final_website_rank.txt', 'w', encoding='utf-8') as final_rank_file:
    for website, score in top_10_websites:
        final_rank_file.write(f"{website}\n")

print("Fin du script.")