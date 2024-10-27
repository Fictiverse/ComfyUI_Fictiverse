from PIL import Image
import numpy as np

class IfImageValid:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "optional": {  
                "if_Valid": ("IMAGE",), 
                "else_Image": ("IMAGE",), 
            },
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("IMAGE",)
    FUNCTION = "selectBestInput"
    CATEGORY = "Fictiverse"

    def selectBestInput(self, if_Valid=None, else_Image=None):
        if if_Valid is not None:
            return (if_Valid,)
        elif else_Image is not None:
            return (else_Image,)
        else:
            return (Image.fromarray(np.zeros((512, 512, 3), dtype=np.uint8)),)         

# Mapping de la classe
NODE_CLASS_MAPPINGS = {
    "If Image Valid": IfImageValid,
}