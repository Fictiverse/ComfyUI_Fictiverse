from PIL import Image
import numpy as np

class IfImageValid:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "optional": {  # Indique que les entrées sont facultatives
                "if_Valid": ("IMAGE",),  # Première image d'entrée (facultative)
                " else_Image": ("IMAGE",),  # Deuxième image d'entrée (facultative)
            },
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("output",)
    FUNCTION = "selectBest"
    CATEGORY = "Fictiverse"

    def selectBest(self, if_Valid=None, else_Image=None):
        # Vérification et retour de l'image appropriée en fonction des valeurs fournies
        if if_Valid is not None and else_Image is None:
            return (if_Valid,)
        elif if_Valid is None and else_Image is not None:
            return (else_Image,)
        elif if_Valid is None and else_Image is None:
            # Retourner une image noire si aucune image n'est fournie
            black_image = Image.fromarray(np.zeros((512, 512, 3), dtype=np.uint8))
            return (black_image,)
        else:
            # Retourner la première image si les deux sont valides
            return (if_Valid,)

# Mapping de la classe
NODE_CLASS_MAPPINGS = {
    "If Image Valid": IfImageValid,
}
