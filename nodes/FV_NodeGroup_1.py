import cv2
import numpy as np
from skimage.exposure import match_histograms
from PIL import Image
from enum import Enum
import torch

# PIL to Tensor
def pil2tensor(image):
    return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0)

# Tensor to PIL
def tensor2pil(image):
    return Image.fromarray(np.clip(255. * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8))
    

class Color_Correction:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "original_image": ("IMAGE",),
                "correction": ("IMAGE",),
                "blend_factor": ("FLOAT", {"default": 1, "min": 0.01, "max": 1.0, "step": 0.01}),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "color_correction"
    CATEGORY = "Fictiverse"

    class BlendType(Enum):
        LUMINOSITY = 1  # Replace with your actual BlendType definition

    def color_correction(self, original_image, correction, blend_factor):

        pil_original_image = np.array(tensor2pil(original_image))
        pil_correction = np.array(tensor2pil(correction))

        original_lab = cv2.cvtColor(pil_original_image, cv2.COLOR_RGB2LAB)
        corrected_lab = cv2.cvtColor(pil_correction, cv2.COLOR_RGB2LAB)
        corrected_image = cv2.cvtColor(match_histograms(original_lab, corrected_lab, channel_axis=2), cv2.COLOR_LAB2RGB).astype("uint8")

        # Use 'correction' as the template image
        template_image = corrected_image  # Use the 'correction' as the template image

        # Perform template matching with 'correction' as the template
        result = cv2.matchTemplate(corrected_image, template_image, cv2.TM_CCOEFF_NORMED)
        
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        top_left = max_loc
        h, w = template_image.shape[:2]
        bottom_right = (top_left[0] + w, top_left[1] + h)
        
        # Draw a rectangle around the matched area (you can modify this part)
        cv2.rectangle(corrected_image, top_left, bottom_right, (0, 0, 255), 2)

        # Apply the blend factor to the result
        blended_image = cv2.addWeighted(pil_original_image, 1 - blend_factor, corrected_image, blend_factor, 0)

        # Convert the result back to a PIL image
        result_image = Image.fromarray(blended_image)

        img = pil2tensor(result_image)
        return (img,)
        
        
class Displace_Image: #Modified version of WAS node : https://github.com/WASasquatch/was-node-suite-comfyui
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "displacement_maps": ("IMAGE",),
                "amplitudeX": ("FLOAT", {"default": 25.0, "min": -4096, "max": 4096, "step": 0.1}),
                "amplitudeY": ("FLOAT", {"default": 25.0, "min": -4096, "max": 4096, "step": 0.1}),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("images",)
    FUNCTION = "displace_image"
    CATEGORY = "Fictiverse"

    def displace_image(self, images, displacement_maps, amplitudeX, amplitudeY):
    
        Tools = Tools_Class()

        displaced_images = []
        for i in range(len(images)):
            img = tensor2pil(images[i])
            if i < len(displacement_maps):
                disp = tensor2pil(displacement_maps[i])
            else:
                disp = tensor2pil(displacement_maps[-1])
            disp = self.resize_and_crop(disp, img.size)
            displaced_images.append(pil2tensor(Tools.displace_image(img, disp, amplitudeX, amplitudeY)))

        displaced_images = torch.cat(displaced_images, dim=0)

        return (displaced_images, )
        
    def resize_and_crop(self, image, target_size):
        width, height = image.size
        target_width, target_height = target_size
        aspect_ratio = width / height
        target_aspect_ratio = target_width / target_height

        if aspect_ratio > target_aspect_ratio:
            new_height = target_height
            new_width = int(new_height * aspect_ratio)
        else:
            new_width = target_width
            new_height = int(new_width / aspect_ratio)

        image = image.resize((new_width, new_height))
        left = (new_width - target_width) // 2
        top = (new_height - target_height) // 2
        right = left + target_width
        bottom = top + target_height
        image = image.crop((left, top, right, bottom))

        return image        
 


class Tools_Class():

    def displace_image(self, image, displacement_map, amplitudeX, amplitudeY):

        image = image.convert('RGB')
        displacement_map = displacement_map.convert('L')
        width, height = image.size
        result = Image.new('RGB', (width, height))

        for y in range(height):
            for x in range(width):

                # Calculate the displacements n' stuff
                displacement = displacement_map.getpixel((x, y))
                displacement_amountX = amplitudeX * (displacement / 255)
                displacement_amountY = amplitudeY * (displacement / 255)
                new_x = x + int(displacement_amountX)
                new_y = y + int(displacement_amountY)

                # Apply mirror reflection at edges and corners
                if new_x < 0:
                    new_x = abs(new_x)
                elif new_x >= width:
                    new_x = 2 * width - new_x - 1

                if new_y < 0:
                    new_y = abs(new_y)
                elif new_y >= height:
                    new_y = 2 * height - new_y - 1

                if new_x < 0:
                    new_x = abs(new_x)
                if new_y < 0:
                    new_y = abs(new_y)

                if new_x >= width:
                    new_x = 2 * width - new_x - 1
                if new_y >= height:
                    new_y = 2 * height - new_y - 1

                # Consider original image color at new location for RGB results, oops
                pixel = image.getpixel((new_x, new_y))
                result.putpixel((x, y), pixel)

        return result  
        
        
        
        
NODE_CLASS_MAPPINGS = {
        "Color correction": Color_Correction,
        "Displace Images with Mask": Displace_Image
}
