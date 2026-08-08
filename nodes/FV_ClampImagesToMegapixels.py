import torch
import torch.nn.functional as F
import math

class ClampImagesMegapixels:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "min_mp": ("FLOAT", {"min": 0.1, "max": 100.0, "step": 0.1, "default": 0.6}),
                "max_mp": ("FLOAT", {"min": 0.1, "max": 100.0, "step": 0.1, "default": 1.0}),
                "multiple_of": ("INT", {"min": 1, "max": 512, "step": 1, "default": 32}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("images",)
    FUNCTION = "run"
    CATEGORY = "Fictiverse/Image"

    def run(self, images, min_mp, max_mp, multiple_of):
        multiple_of = max(1, multiple_of)

        if images is None or not isinstance(images, torch.Tensor):
            return (images,)

        if len(images.shape) != 4 or images.shape[1] <= 0 or images.shape[2] <= 0:
            return (images,)

        B, H, W, C = images.shape
        current_pixels = H * W
        
        limit_upper_pixels = int(max_mp * 1_000_000)
        limit_lower_pixels = int(min_mp * 1_000_000)
        
        target_pixels = max(limit_lower_pixels, min(current_pixels, limit_upper_pixels))
        
        aspect_ratio = W / H
        new_height = math.sqrt(target_pixels / aspect_ratio)
        new_width = new_height * aspect_ratio

        new_width = max(multiple_of, int(round(new_width / multiple_of) * multiple_of))
        new_height = max(multiple_of, int(round(new_height / multiple_of) * multiple_of))
        
        if new_height == H and new_width == W:
             return (images,)

        img_batch = images.permute(0, 3, 1, 2)
        
        if img_batch.dtype != torch.float32:
            img_batch = img_batch.float()
        
        resized = F.interpolate(img_batch, size=(new_height, new_width), mode='bilinear', align_corners=False)
        resized = resized.permute(0, 2, 3, 1).to(images.dtype)

        return (resized,)

NODE_CLASS_MAPPINGS = {
    "Clamp Images To Megapixels": ClampImagesMegapixels
}