import numpy as np
from PIL import Image
from PIL.PngImagePlugin import PngInfo
import folder_paths
import os
import base64
import torch
import re
from datetime import datetime

# ==========================================
# ALGORITHME D'ENCODAGE / DECODAGE
# ==========================================
def encode_prompt(text, password):
    if not password or not text:
        return text
    text_bytes = text.encode('utf-8')
    key_bytes = password.encode('utf-8')
    encoded = bytearray(len(text_bytes))
    for i in range(len(text_bytes)):
        encoded[i] = text_bytes[i] ^ key_bytes[i % len(key_bytes)]
    return base64.b64encode(encoded).decode('utf-8')

def decode_prompt(encoded_text, password):
    if not password or not encoded_text:
        return encoded_text
    try:
        decoded_bytes = base64.b64decode(encoded_text)
        key_bytes = password.encode('utf-8')
        decoded = bytearray(len(decoded_bytes))
        for i in range(len(decoded_bytes)):
            decoded[i] = decoded_bytes[i] ^ key_bytes[i % len(key_bytes)]
        return decoded.decode('utf-8')
    except Exception as e:
        return "" # Renvoie un texte vide en cas d'erreur de décodage

# ==========================================
# GESTION DES DATES POUR LE NOM DE FICHIER
# ==========================================
def process_filename_tags(text, width, height):
    pattern = r"%date:(.*?)%"
    def replace_date(match):
        fmt = match.group(1)
        fmt = fmt.replace("yyyy", "%Y").replace("yy", "%y")
        fmt = fmt.replace("MM", "%m").replace("dd", "%d")
        fmt = fmt.replace("hh", "%H").replace("mm", "%M").replace("ss", "%S")
        return datetime.now().strftime(fmt)
    
    text = re.sub(pattern, replace_date, text)
    text = text.replace("%width%", str(width))
    text = text.replace("%height%", str(height))
    return text


# ==========================================
# NODE 1 : SAUVEGARDER L'IMAGE (PASSWORD)
# ==========================================
class Save_Image_Password:
    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()
        self.type = "output"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "prompt": ("STRING",),
                "password": ("STRING",),
                "filename_prefix": ("STRING", {"default": "Images/%date:yy-MM-dd%/%date:hhmmss%_"}),
                "image_format": (["JPG", "PNG"], {"default": "JPG"}),
            }
        }

    RETURN_TYPES = ()
    FUNCTION = "save_images"
    OUTPUT_NODE = True
    CATEGORY = "Fictiverse/Image"

    def save_images(self, images, prompt, password, filename_prefix="Secret", image_format="JPG"):

        jpeg_qual = 70
        png_comp = 9

        width, height = images[0].shape[1], images[0].shape[0]
        filename_prefix = process_filename_tags(filename_prefix, width, height)

        subfolder = os.path.dirname(os.path.normpath(filename_prefix))
        filename = os.path.basename(os.path.normpath(filename_prefix))
        full_output_folder = os.path.join(self.output_dir, subfolder)

        if os.path.commonpath((self.output_dir, os.path.abspath(full_output_folder))) != self.output_dir:
            print("Erreur: Sauvegarde en dehors du dossier output non autorisée.")
            return {}

        os.makedirs(full_output_folder, exist_ok=True)

        def map_filename(f):
            prefix_len = len(filename)
            prefix = f[:prefix_len]
            try:
                digits = int(f[prefix_len:].split('_')[0])
            except:
                digits = 0
            return (digits, prefix)

        try:
            counter = max(
                filter(
                    lambda a: a[1] == filename,
                    map(map_filename, os.listdir(full_output_folder))
                )
            )[0] + 1
        except (ValueError, FileNotFoundError):
            counter = 1

        results = list()
        encrypted_prompt = encode_prompt(prompt, password)

        ext = ".png" if image_format == "PNG" else ".jpg"

        for image in images:
            i = 255.0 * image.cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))

            file = f"{filename}{counter:05}_{ext}"
            file_path = os.path.join(full_output_folder, file)
            
            if image_format == "PNG":
                metadata = PngInfo()
                metadata.add_text("prompt", encrypted_prompt)
                img.save(file_path, pnginfo=metadata, compress_level=png_comp)
            else:
                exif = img.getexif()
                exif[0x010E] = encrypted_prompt # 0x010E = ImageDescription
                img.save(file_path, quality=jpeg_qual, exif=exif)

            results.append({
                "filename": file,
                "subfolder": subfolder,
                "type": self.type
            })
            counter += 1

        return {"ui": {"images": results}}


# ==========================================
# FONCTION COMMUNE DE LECTURE (JPEG & PNG)
# ==========================================
def extract_prompt_from_image(img, password):
    prompt = "" # Renvoie un texte vide si rien n'est trouvé
    
    if img.format == "PNG":
        if "prompt" in img.info:
            prompt = decode_prompt(img.info["prompt"], password)
    else:
        exif = img.getexif()
        if exif is not None and 0x010E in exif:
            prompt = decode_prompt(exif[0x010E], password)
            
    return prompt


# ==========================================
# NODE 2 : CHARGER IMAGE & LIRE PROMPT (UPLOAD)
# ==========================================
class Load_Image_Password:
    @classmethod
    def INPUT_TYPES(cls):
        input_dir = folder_paths.get_input_directory()
        files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]
        return {
            "required": {
                "image_file": (sorted(files), {"image_upload": True}),
                "password": ("STRING",),
            }
        }

    RETURN_TYPES = ("IMAGE", "STRING")
    RETURN_NAMES = ("image", "prompt")
    FUNCTION = "load_and_decode"
    CATEGORY = "Fictiverse/Image"

    def load_and_decode(self, image_file, password):
        image_path = folder_paths.get_annotated_filepath(image_file)
        img = Image.open(image_path)
        
        prompt = extract_prompt_from_image(img, password)

        img = img.convert("RGB")
        image_tensor = torch.from_numpy(np.array(img).astype(np.float32) / 255.0)[None,]

        return (image_tensor, prompt)


# ==========================================
# MAPPINGS COMFYUI
# ==========================================
NODE_CLASS_MAPPINGS = {
    "Save Image with Password Prompt": Save_Image_Password,
    "Load Image with Password Prompt": Load_Image_Password
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Save Image with Password Prompt": "Save Image with Password Prompt",
    "Load Image with Password Prompt": "Load Image with Password Prompt"
}