class IsImageValid:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "optional": {
                "image": ("IMAGE",),  # Type d'entrée défini comme IMAGE
            },
        }

    RETURN_TYPES = ("BOOL",)
    RETURN_NAMES = ("is_valid",)
    FUNCTION = "check_is_valid"
    CATEGORY = "Fictiverse"

    def check_is_valid(self, image=None):
        # Retourne False si l'image est None, sinon True
        return (image is not None,)

# Mapping de la classe
NODE_CLASS_MAPPINGS = {
    "Is Image Valid ?": IsImageValid,
}
