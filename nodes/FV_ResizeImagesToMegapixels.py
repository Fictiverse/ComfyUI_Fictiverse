import torch
import torch.nn.functional as F
import math

class ResizeImagesToMegapixels:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),  # batch of images: [B, H, W, C]
                "megapixels": ("FLOAT", {"min": 0.1, "max": 100.0, "step": 0.1, "default": 1.0}),
                "multiple_of": ("INT", {"min": 1, "max": 512, "step": 1, "default": 64}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("images",)
    FUNCTION = "run"
    CATEGORY = "Fictiverse/Resize"

    def run(self, images, megapixels, multiple_of):
        # images shape: [B, H, W, C] -> we convert to [B, C, H, W] for F.interpolate
        img_batch = images.permute(0, 3, 1, 2).float()  # convert to float for interpolation
        B, C, H, W = img_batch.shape
        aspect_ratio = W / H
        target_pixels = int(megapixels * 1_000_000)

        # Compute new dimensions
        new_height = math.sqrt(target_pixels / aspect_ratio)
        new_width = new_height * aspect_ratio

        # Round to multiple_of
        new_width = int(round(new_width / multiple_of) * multiple_of)
        new_height = int(round(new_height / multiple_of) * multiple_of)

        # Resize batch using bilinear interpolation
        resized = F.interpolate(img_batch, size=(new_height, new_width), mode='bilinear', align_corners=False)

        # Convert back to [B, H, W, C] and uint8 if necessary
        resized = resized.permute(0, 2, 3, 1).to(images.dtype)

        return (resized,)


# Register the node
NODE_CLASS_MAPPINGS = {
    "Resize Images To Megapixels": ResizeImagesToMegapixels
}
