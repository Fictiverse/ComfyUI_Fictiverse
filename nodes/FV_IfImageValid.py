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
                "else": ("IMAGE",),  # Deuxième image d'entrée (facultative)
            },
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("output",)
    FUNCTION = "selectBest"
    CATEGORY = "Fictiverse"

    def selectBest(self, input1=None, input2=None):
        # Vérification et retour de l'image appropriée en fonction des valeurs fournies
        if input1 is not None and input2 is None:
            return (input1,)
        elif input1 is None and input2 is not None:
            return (input2,)
        elif input1 is None and input2 is None:
            # Retourner une image noire si aucune image n'est fournie
            black_image = Image.fromarray(np.zeros((512, 512, 3), dtype=np.uint8))
            return (black_image,)
        else:
            # Retourner la première image si les deux sont valides
            return (input1,)

# Mapping de la classe
NODE_CLASS_MAPPINGS = {
    "If Image Valid": IfImageValid,
}
