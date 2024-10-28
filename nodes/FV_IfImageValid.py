import numpy as np
import torch

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
            black_image = torch.zeros((1, 32, 32, 3), dtype=torch.uint8) 
            return (black_image,)

# Mapping de la classe
NODE_CLASS_MAPPINGS = {
    "If Image Valid": IfImageValid,
}
