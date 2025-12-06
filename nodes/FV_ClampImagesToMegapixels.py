import torch
import torch.nn.functional as F
import math

class ClampImagesMegapixels:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),  # batch [B, H, W, C]
                "min_mp": ("FLOAT", {"min": 0.1, "max": 100.0, "step": 0.1, "default": 0.6}),
                "max_mp": ("FLOAT", {"min": 0.1, "max": 100.0, "step": 0.1, "default": 1.0}),
                "multiple_of": ("INT", {"min": 1, "max": 512, "step": 1, "default": 64}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("images",)
    FUNCTION = "run"
    CATEGORY = "Fictiverse/Resize"

    def run(self, images, min_mp, max_mp, multiple_of):
        B, H, W, C = images.shape
        current_pixels = H * W
        
        # Conversion MP -> Pixels absolus
        limit_upper_pixels = int(max_mp * 1_000_000)
        limit_lower_pixels = int(min_mp * 1_000_000)
        
        # 1. Définir la cible (Clamp)
        # Si < min, on vise min.
        # Si > max, on vise max.
        # Sinon, on vise la taille actuelle.
        target_pixels = current_pixels
        if target_pixels < limit_lower_pixels:
            target_pixels = limit_lower_pixels
        elif target_pixels > limit_upper_pixels:
            target_pixels = limit_upper_pixels
        
        # Préparation calculs dimensions
        aspect_ratio = W / H
        new_height = math.sqrt(target_pixels / aspect_ratio)
        new_width = new_height * aspect_ratio

        # 2. Quantification Spatiale (Arrondi au multiple de 'multiple_of')
        new_width = int(round(new_width / multiple_of) * multiple_of)
        new_height = int(round(new_height / multiple_of) * multiple_of)
        
        # Optimisation : Si les dimensions calculées sont identiques à l'original, on renvoie l'original
        if new_height == H and new_width == W:
             return (images,)

        # 3. Exécution du Resize
        # Conversion [B, H, W, C] -> [B, C, H, W] pour pytorch
        img_batch = images.permute(0, 3, 1, 2).float()
        
        resized = F.interpolate(img_batch, size=(new_height, new_width), mode='bilinear', align_corners=False)

        # Retour au format ComfyUI [B, H, W, C]
        resized = resized.permute(0, 2, 3, 1).to(images.dtype)

        return (resized,)

# Enregistrement de la node
NODE_CLASS_MAPPINGS = {
    "Clamp Images To Megapixels": ClampImagesMegapixels
}