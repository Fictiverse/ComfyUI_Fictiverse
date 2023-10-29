import cv2
import numpy as np
from PIL import Image
from skimage import exposure

class ColorCorrection:
    """
    This node provides a simple interface to apply PixelSort blur to the output image.
    """
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "original_image": ("IMAGE",),
                }),
            },
        }
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "color_correction"
    CATEGORY = "Fictiverse"


    def color_correction(self, image, original_image):
        correction_target = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2LAB)
        corrected_image = cv2.cvtColor(exposure.match_histograms(
            cv2.cvtColor(np.asarray(original_image), cv2.COLOR_RGB2LAB),
            correction_target,
            channel_axis=2
        ), cv2.COLOR_LAB2RGB).astype("uint8")
        #inverted_image = self.invert_image(corrected_image)
        return (corrected_image,)


    #def invert_image(self, image):
    #    inverted_image = 1.0 - image
    #    return inverted_image
        

# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "Color correction": ColorCorrect
}

