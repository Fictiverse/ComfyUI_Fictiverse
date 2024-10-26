class ScaleSelector:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "768x768": ("BOOLEAN", {"default": False}),
                "1280x800": ("BOOLEAN", {"default": False}),
                "864x1280": ("BOOLEAN", {"default": False}),
                "1024x1024": ("BOOLEAN", {"default": True}),
                "1536x800": ("BOOLEAN", {"default": True}),
                "1920x1088": ("BOOLEAN", {"default": False}),
                "1088x1920": ("BOOLEAN", {"default": False}),
                # Ajoutez d'autres résolutions utiles si nécessaire
            },
        }

    RETURN_TYPES = ("INT", "INT")  # Returning width and height as separate outputs
    RETURN_NAMES = ("width", "height")
    FUNCTION = "select_resolution"
    CATEGORY = "Fictiverse"

    def select_resolution(self, **kwargs):
        # Initialize variables for the maximum resolution
        max_width = 0
        max_height = 0

        # Check which resolutions are selected based on the boolean values
        for resolution, selected in kwargs.items():
            if selected:
                width, height = map(int, resolution.split('x'))
                # Update max_width and max_height if the current resolution is larger
                if width > max_width or height > max_height:
                    max_width, max_height = width, height

        # Return the maximum resolution found, or default dimensions if none selected
        if max_width > 0 and max_height > 0:
            return (max_width, max_height)
        else:
            # Default dimensions if no resolution is selected
            return (1024, 1024)



NODE_CLASS_MAPPINGS = {
    "Scale Selector": ScaleSelector,
}
