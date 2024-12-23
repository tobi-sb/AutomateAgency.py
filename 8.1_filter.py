import os
from PIL import Image, ImageFile
import shutil
import torch
import open_clip
import numpy as np
import torch.nn.functional as F
import cairosvg
from io import BytesIO

ImageFile.LOAD_TRUNCATED_IMAGES = True

class ImageDescriptionBot:
    def __init__(self, images_directory):
        self.images_directory = images_directory
        self.filtered_directory = "./images_filter1"
        if os.path.exists(self.filtered_directory):
            shutil.rmtree(self.filtered_directory)
        os.makedirs(self.filtered_directory, exist_ok=True)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model, _, self.preprocess = open_clip.create_model_and_transforms("ViT-B-32", pretrained="laion2b_s34b_b79k", device=self.device)
        self.descriptions = [
            "A photo of an object.",
            "A general scene.",
            "A person or group of people.",
            "An outdoor view.",
            "An indoor setting.",
            "A logo for a website", 
            "An animal or pet.",
            "A building or structure.",
            "A night or day view.",
            "A food or drink item.",
            "A vehicle of some kind.",
            "A festive or decorated setting.",
            "An activity or event.",
            "A plant or flower.",
        ]

    def get_image_descriptions(self):
        image_descriptions = {}
        for image_name in os.listdir(self.images_directory):
            image_path = os.path.join(self.images_directory, image_name)
            if os.path.isfile(image_path) and image_name.lower().endswith(('.png', '.jpg', '.jpeg', '.svg')):
                try:
                    if image_name.lower().endswith('.svg'):
                        # Convert SVG to PNG
                        png_data = cairosvg.svg2png(url=image_path, output_width=256, output_height=256)
                        image = Image.open(BytesIO(png_data))
                    else:
                        image = Image.open(image_path)

                    image_input = self.preprocess(image).unsqueeze(0).to(self.device)

                    with torch.no_grad():
                        image_features = self.model.encode_image(image_input)

                    description = self._get_best_description(image_features)
                    image_descriptions[image_name] = description

                    if description == "A logo for a website":
                        self._copy_to_filtered_directory(image_path, image_name)
                except OSError as e:
                    print(f"Error processing {image_name}: {e}")
                except ValueError as e:
                    print(f"Error processing {image_name}: {e}")
        return image_descriptions

    def _get_best_description(self, image_features):
        text_tokens = open_clip.tokenize(self.descriptions).to(self.device)
        with torch.no_grad():
            text_features = self.model.encode_text(text_tokens)

        # Compute cosine similarity between image features and text features
        image_features = F.normalize(image_features, p=2, dim=-1)
        text_features = F.normalize(text_features, p=2, dim=-1)
        similarities = torch.matmul(image_features, text_features.T).squeeze(0)

        # Get the index of the most similar description
        best_idx = torch.argmax(similarities).item()
        return self.descriptions[best_idx]

    def _copy_to_filtered_directory(self, image_path, image_name):
        shutil.copy(image_path, os.path.join(self.filtered_directory, image_name))

if __name__ == "__main__":
    bot = ImageDescriptionBot("./images")
    descriptions = bot.get_image_descriptions()
    for img_name, desc in descriptions.items():
        print(f"{img_name}: {desc}")