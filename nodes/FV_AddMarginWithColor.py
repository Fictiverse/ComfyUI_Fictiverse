import torch

class AddMarginWithColor:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",), 
                "margin_pct": ("INT", {"default": 10, "min": 0, "max": 100}),
                "top": ("BOOLEAN", {"default": False, "label_on": "Top Active", "label_off": "Bottom Active"}),
                "black": ("BOOLEAN", {"default": True, "label_on": "Black Margin", "label_off": "White Margin"}),
            },
        }

    RETURN_TYPES = ("IMAGE", "MASK")
    RETURN_NAMES = ("OUTPUT_IMAGE", "MASK")
    FUNCTION = "add_margin_with_color"
    CATEGORY = "Fictiverse/ImageProcessing"

    def add_margin_with_color(self, image, margin_pct=10, top=False, black=True):
        # Choose the color based on the boolean value
        color = "#000000" if black else "#FFFFFF"
        
        # Convert color from hex to RGB
        rgb = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))  # Extract RGB from hex
        color_tensor = torch.tensor(rgb, dtype=image.dtype).view(1, 1, 1, 3)

        # Image dimensions
        _, h, w, c = image.shape

        # Calculate margin size in pixels based on percentage
        margin_height = int(h * (margin_pct / 100))

        # Define new dimensions with the added margin
        new_height = h + margin_height
        new_width = w

        # Expand color tensor to fill the new image size with the margin
        output_image = color_tensor.expand(1, new_height, new_width, 3).clone()

        # Create a mask with 1s in the area of the original image and 0s in the margin area
        mask = torch.zeros((1, new_height, new_width), dtype=torch.uint8)
        
        # Determine starting position based on top or bottom margin option
        start_y = margin_height if top else 0

        # Place the original image in the new tensor and set the mask
        output_image[:, start_y:start_y + h, :, :] = image
        mask[:, start_y:start_y + h, :] = 1

        return output_image, mask

# Class Mapping
NODE_CLASS_MAPPINGS = {
    "Add Margin With Color": AddMarginWithColor,
}
