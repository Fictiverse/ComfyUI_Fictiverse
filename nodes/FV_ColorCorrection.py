import cv2
import numpy as np
from skimage.exposure import match_histograms
from PIL import Image
from enum import Enum
import torch

# Tensor to PIL
def tensor2pil(image):
    return Image.fromarray(np.clip(255. * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8))

# Define 'BlendType' and 'blendLayers' as needed
def blendLayers(image1, image2):
    # Extract the luminance channel from both images
    image1_luminance = image1.convert("L")
    image2_luminance = image2.convert("L")

    # Combine the luminance channel from image1 with the color channels of image2
    r, g, b = image2.split()
    blended_image = Image.merge("RGB", [image1_luminance, g, b])

    return blended_image


class ColorCorrection:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "original_image": ("IMAGE",),
                "correction": ("IMAGE",),  # Add this line
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "color_correction"
    CATEGORY = "Fictiverse"


        
        
    def color_correction(self, original_image, correction):
        
        pil_original_image = np.array(tensor2pil(original_image))
        pil_correction = np.array(tensor2pil(correction))
        
        # Perform color correction
        original_lab = cv2.cvtColor(pil_original_image, cv2.COLOR_RGB2LAB)
        corrected_lab = cv2.cvtColor(pil_correction, cv2.COLOR_RGB2LAB)
        corrected_image = cv2.cvtColor(match_histograms(original_lab, corrected_lab, channel_axis=2), cv2.COLOR_LAB2RGB).astype("uint8")

        # You need to implement the blendLayers function and BlendType.LUMINOSITY.
        # The following line assumes that it exists in your code:
        image = blendLayers(Image.fromarray(corrected_image), Image.fromarray(pil_original_image))
        
        #Return image is in wrong type ?
        return (image,)

    
NODE_CLASS_MAPPINGS = {
    "Color correction": ColorCorrection
}