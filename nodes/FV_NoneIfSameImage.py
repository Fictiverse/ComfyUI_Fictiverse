import torch
import numpy as np

class NoneIfSameImage:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "optional": {  
                "image": ("IMAGE",),
                "compare": ("IMAGE",),
            },
        }

    RETURN_TYPES = ("IMAGE", "BOOL",)
    RETURN_NAMES = ("IMAGE", "is_same",)
    FUNCTION = "checkIfSameImage"
    CATEGORY = "Fictiverse"

    def checkIfSameImage(self, image=None, compare=None):
        if image is None and compare is None:
            black_image = torch.zeros((1, 32, 32, 3), dtype=torch.uint8) 
            return (black_image, False)

        if image is None:
            return (compare, False)

        if compare is None:
            return (image, False)

        if torch.equal(image, compare):
            black_image = torch.zeros((1, 32, 32, 3), dtype=torch.uint8) 
            return (black_image, True)

        return (image, False)

NODE_CLASS_MAPPINGS = {
    "None if same Image": NoneIfSameImage,
}
