import math

class ResizeToMegapixels:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "width": ("INT", {"min": 64, "max": 8192, "step": 1, "default": 1024}),
                "height": ("INT", {"min": 64, "max": 8192, "step": 1, "default": 1024}),
                "megapixels": ("FLOAT", {"min": 0.1, "max": 100.0, "step": 0.1, "default": 1.0}),
                "multiple_of": ("INT", {"min": 1, "max": 512, "step": 1, "default": 64}),
            }
        }

    RETURN_TYPES = ("INT", "INT")
    RETURN_NAMES = ("adjusted_width", "adjusted_height")
    FUNCTION = "run"
    CATEGORY = "Fictiverse/Resize"

    def run(self, width, height, megapixels, multiple_of):
        aspect_ratio = width / height
        target_pixels = int(megapixels * 1_000_000)

        # Nouvelle hauteur basée sur la cible de pixels et le ratio
        new_height = math.sqrt(target_pixels / aspect_ratio)
        new_width = new_height * aspect_ratio

        # On arrondit aux multiples
        new_width = int(round(new_width / multiple_of) * multiple_of)
        new_height = int(round(new_height / multiple_of) * multiple_of)

        return (new_width, new_height)

# Enregistrement de la node
NODE_CLASS_MAPPINGS = {
    "Resize To Megapixels": ResizeToMegapixels
}
