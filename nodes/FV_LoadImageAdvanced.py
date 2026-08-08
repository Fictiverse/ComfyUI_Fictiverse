import os
import numpy as np
import torch
from PIL import Image
import folder_paths

RATIOS = ["1:1", "5:4", "4:3", "3:2", "16:9", "2:1", "21:9", "32:9"]


def ensure_multiple_of_32(img):
    """Ajuste les dimensions d'une image PIL pour qu'elles soient multiples de 32."""
    w, h = img.size
    if w % 32 != 0 or h % 32 != 0:
        w_new = max(32, int(round(w / 32.0) * 32))
        h_new = max(32, int(round(h / 32.0) * 32))
        return img.resize((w_new, h_new), Image.Resampling.LANCZOS)
    return img


def calculate_dimensions(ratio_str, portrait, target_megapixel):
    """Calcule les dimensions (largeur, hauteur) arrondies à un multiple de 32."""
    try:
        w_ratio, h_ratio = map(float, ratio_str.split(":"))
    except ValueError:
        w_ratio, h_ratio = 1.0, 1.0

    if portrait:
        w_ratio, h_ratio = h_ratio, w_ratio

    aspect_ratio = w_ratio / h_ratio
    target_pixels = target_megapixel * 1_000_000

    h = np.sqrt(target_pixels / aspect_ratio)
    w = aspect_ratio * h

    w = max(32, int(round(w / 32.0) * 32))
    h = max(32, int(round(h / 32.0) * 32))
    return w, h


def scale_to_megapixel(img, target_megapixel):
    """Redimensionne une image PIL selon un nombre de mégapixels cible, multiple de 32."""
    w_orig, h_orig = img.size
    aspect_ratio = w_orig / h_orig
    target_pixels = target_megapixel * 1_000_000

    h = np.sqrt(target_pixels / aspect_ratio)
    w = aspect_ratio * h

    w = max(32, int(round(w / 32.0) * 32))
    h = max(32, int(round(h / 32.0) * 32))
    return img.resize((w, h), Image.Resampling.LANCZOS)


class Load_Image_Advanced:
    @classmethod
    def INPUT_TYPES(cls):
        input_dir = folder_paths.get_input_directory()
        files = [
            f
            for f in os.listdir(input_dir)
            if os.path.isfile(os.path.join(input_dir, f))
        ]
        return {
            "required": {
                "image_file": (sorted(files), {"image_upload": True}),
                "enable": (
                    "BOOLEAN",
                    {
                        "default": True,
                        "label_on": "Enabled 🟢",
                        "label_off": "Disabled 🔴",
                    },
                ),
                "scale_image": ("BOOLEAN", {"default": False}),
                "megapixel": (
                    "FLOAT",
                    {"default": 1.0, "min": 0.1, "max": 16.0, "step": 0.1},
                ),
                "ratio": (RATIOS, {"default": "1:1"}),
                "orientation": (
                    "BOOLEAN",
                    {
                        "default": False,
                        "label_on": "Portrait ▯",
                        "label_off": "Landscape ▭",
                    },
                ),
            }
        }

    RETURN_TYPES = ("IMAGE_PARAMS",)
    RETURN_NAMES = ("_",)
    FUNCTION = "run"
    CATEGORY = "Fictiverse/Image"

    def run(self, image_file, enable, scale_image, megapixel, ratio, orientation):
        if enable:
            image_path = folder_paths.get_annotated_filepath(image_file)
            img = Image.open(image_path)
            img = img.convert("RGB")

            if scale_image:
                img = scale_to_megapixel(img, megapixel)
            else:
                img = ensure_multiple_of_32(img)

            w, h = img.size
        else:
            w, h = calculate_dimensions(ratio, orientation, megapixel)
            img = Image.new("RGB", (w, h), (0, 0, 0))

        image_tensor = torch.from_numpy(
            np.array(img).astype(np.float32) / 255.0
        )[None,]

        # Compactage de tous les paramètres et de l'image
        params = {
            "image": image_tensor,
            "width": w,
            "height": h,
            "megapixel": megapixel,
            "enabled": enable,
        }

        return (params,)



class Load_Image_Bypass:
    @classmethod
    def INPUT_TYPES(cls):
        input_dir = folder_paths.get_input_directory()
        
        # Extensions d'images et de GIFs supportées par PIL
        valid_extensions = {'.png', '.jpg', '.jpeg', '.webp', '.bmp', '.tiff', '.gif', '.apng'}
        
        files = [
            f for f in os.listdir(input_dir)
            if os.path.isfile(os.path.join(input_dir, f)) 
            and os.path.splitext(f)[1].lower() in valid_extensions
        ]
        
        return {
            "required": {
                "image_file": (sorted(files), {"image_upload": True}),
                "enable": (
                    "BOOLEAN",
                    {
                        "default": True,
                        "label_on": "Active 🟢",
                        "label_off": "Disabled 🔴",
                    },
                ),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = "run"
    CATEGORY = "Fictiverse/Image"

    def run(self, image_file, enable):
        # Si désactivé, on retourne (None,) pour interrompre la branche dans ComfyUI
        if not enable:
            return (None,)

        image_path = folder_paths.get_annotated_filepath(image_file)
        img = Image.open(image_path)
        img = img.convert("RGB")
        img = ensure_multiple_of_32(img)

        image_tensor = torch.from_numpy(
            np.array(img).astype(np.float32) / 255.0
        )[None,]

        return (image_tensor,)


class Unpack_Image_Params:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "params": ("IMAGE_PARAMS",),
            }
        }

    RETURN_TYPES = ("IMAGE", "INT", "INT", "FLOAT", "BOOLEAN")
    RETURN_NAMES = ("image", "width", "height", "megapixel", "enabled")
    FUNCTION = "unpack"
    CATEGORY = "Fictiverse/Image"

    def unpack(self, params):
        image = params.get("image")
        if image is None:
            image = torch.zeros((1, 512, 512, 3), dtype=torch.float32)

        return (
            image,
            params.get("width", 512),
            params.get("height", 512),
            params.get("megapixel", 1.0),
            params.get("enabled", True),
        )


# ==========================================
# MAPPINGS COMFYUI
# ==========================================
NODE_CLASS_MAPPINGS = {
    "LoadImageAdvanced": Load_Image_Advanced,
    "LoadImageBypass": Load_Image_Bypass,
    "UnpackImageParams": Unpack_Image_Params,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LoadImageAdvanced": "Load Image Advanced",
    "LoadImageBypass": "Load Image Bypass",
    "UnpackImageParams": "Unpack Image Params",
}