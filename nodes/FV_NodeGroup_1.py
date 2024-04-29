from re import S
import cv2
import numpy as np
from skimage.exposure import match_histograms
from PIL import Image
from enum import Enum
import torch
import torch.nn.functional as F
from torchvision import transforms
from random import randint

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
            disp = Tools.resize_and_crop(disp, img.size)
            displaced_images.append(pil2tensor(Tools.displace_imageNP(img, disp, amplitudeX, amplitudeY)))

        displaced_images = torch.cat(displaced_images, dim=0)

        return (displaced_images, )     
 





class AddNoiseToImageWithMask: #Modified version of WAS node : https://github.com/WASasquatch/was-node-suite-comfyui
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "masks": ("IMAGE",),
                "strength": ("FLOAT", {"default": 0.5, "min": 0, "max": 1, "step": 0.05}),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("images",)
    FUNCTION = "addNoiseToImageWithMask"
    CATEGORY = "Fictiverse"

    def addNoiseToImageWithMask(self, images, masks, strength):
    
        Tools = Tools_Class()

        out_images = []
        for i in range(len(images)):
            img = tensor2pil(images[i])
            if i < len(masks):
                mask = tensor2pil(masks[i])
            else:
                mask = tensor2pil(masks[-1])
            mask = Tools.resize_and_crop(mask, img.size)
            out_images.append(pil2tensor(Tools.add_noise_with_mask(img, mask, strength)))

        out_images = torch.cat(out_images, dim=0)

        return (out_images, )
        



####################################################################   

class DisplaceImageWithDepth: #Modified version of WAS node : https://github.com/WASasquatch/was-node-suite-comfyui
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Image": ("IMAGE",),
                "Depth": ("IMAGE",),
                "X": ("INT", {"default": 0, "min": -4096, "max": 4096, "step": 1}),
                "Y": ("INT", {"default": 0, "min": -4096, "max": 4096, "step": 1}),
                "Zoom": ("FLOAT", {"default": 0.0, "min": -1, "max": 1, "step": 0.1}),
                "Rotation": ("FLOAT", {"default": 0.0, "min": -90, "max": 90, "step": 1}),
                "Shake": ("INT", {"default": 0, "min": 0, "max": 100, "step": 1}),
                "LayerCount": ("INT", {"default": 8, "min": 2, "max": 255, "step": 1}),
                "Frames": ("INT", {"default": 4, "min": 2, "max": 128, "step": 1}),
                "Fill": ("BOOLEAN", {"default": True, "label_on": "Yes", "label_off": "No"}),
            },
        }

    RETURN_TYPES = ("IMAGE","IMAGE",)
    RETURN_NAMES = ("Frames", "Layers",)
    FUNCTION = "displaceImageWithDepth"
    CATEGORY = "Fictiverse"

    def displaceImageWithDepth(self, Image, Depth, X, Y, Zoom, Rotation, Shake, LayerCount, Frames, Fill):
    
        Tools = Tools_Class()

        result_layers = []
        result_images = []
        img = tensor2pil(Image[0])
        mask = tensor2pil(Depth[0])
        mask = Tools.resize_and_crop(mask, img.size)

        shakeX = 0
        shakeY = 0
        fX = X/Frames
        fY = Y/Frames  
        fZ = Zoom/Frames  
        
        for f in range(Frames): 
            
            shakeX = shakeX + np.random.randint(low=-100, high=100)
            shakeY = shakeY + np.random.randint(low=-100, high=100)
            
            tx = fX * f + shakeX*(Shake/100)
            ty = fY * f + shakeY*(Shake/100)
            z = fZ * f
            layers, combined = Tools.apply_perspective_transformation(img, mask, tx, ty, z, LayerCount, Fill)
            result_images.append(pil2tensor(combined))
            
            if f == 0:
                for layer in layers:
                    result_layers.append(pil2tensor(layer))

        result_layers = torch.cat(result_layers, dim=0)
        result_images = torch.cat(result_images, dim=0)
        
        return (result_images, result_layers)
    
####################################################################




class ZoomWithDepth:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Image": ("IMAGE",),
                "Depth": ("IMAGE",),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = "zoomWithDepth"
    CATEGORY = "Fictiverse"

    def zoomWithDepth(self, Image, Depth):
    
        Tools = Tools_Class()

        img = tensor2pil(Image[0])
        mask = tensor2pil(Depth[0])
        mask = Tools.resize_and_crop(mask, img.size)
        
        combined= Tools.parallax_zoom(img, mask)


        return ( pil2tensor(combined))
####################################################################



class Tools_Class():
    
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


    def displace_imageNP(self, image, displacement_map, amplitudeX, amplitudeY):
        image = image.convert('RGB')
        displacement_map = displacement_map.convert('L')

        # Convert PIL images to NumPy arrays
        image_arr = np.array(image)
        displacement_arr = np.array(displacement_map)

        height, width, _ = image_arr.shape
        result_arr = np.zeros((height, width, 3), dtype=np.uint8)

        # Calculate displacements
        displacement_normalized = displacement_arr / 255.0
        displacement_amountX = amplitudeX * displacement_normalized
        displacement_amountY = amplitudeY * displacement_normalized

        # Create grids of x and y coordinates
        x_coords, y_coords = np.meshgrid(np.arange(width), np.arange(height))

        # Calculate new coordinates
        new_x = np.clip(x_coords + displacement_amountX, 0, width - 1).astype(int)
        new_y = np.clip(y_coords + displacement_amountY, 0, height - 1).astype(int)

        # Apply mirror reflection at edges and corners
        new_x = np.where(new_x < 0, -new_x, new_x)
        new_x = np.where(new_x >= width, 2 * width - new_x - 1, new_x)
        new_y = np.where(new_y < 0, -new_y, new_y)
        new_y = np.where(new_y >= height, 2 * height - new_y - 1, new_y)

        # Fetch pixels from original image at new locations
        result_arr = image_arr[new_y, new_x]

        # Create PIL Image from NumPy array
        result = Image.fromarray(result_arr)

        return result











    def displaceImageWithDepth(self, image, mask, amplitudeX, amplitudeY, amplitudeZ, layerCount):

        image = image.convert('RGB')
        mask = mask.convert('L')
        width, height = image.size

        layerStep = int(255/layerCount)
        imageLayers = []
        
        for l in range(layerCount):
        
            layer = Image.new('RGBA', (width, height))
            colorTarget = max(0, min(l*layerStep, 255))
            colorRangeMin = max(0, min(colorTarget-layerStep, 255))
            colorRangeMax = max(0, min(colorTarget+layerStep, 255))
            colorRange = range(colorRangeMin, colorRangeMax, 1)
          
            for y in range(height):
                for x in range(width):        
                    maskValue = mask.getpixel((x, y))
                    if maskValue in colorRange:
                        
                        amplitude = l/layerCount
                        offsetX = int(amplitudeX*amplitude*amplitude)
                        offsetY = int(amplitudeY*amplitude*amplitude)
                        offsetZ = int(amplitudeZ*amplitude*amplitude)
                        nX = x+offsetX
                        nY = y+offsetY

                        if nX >=0 and nX<width and nY >=0 and nY<height:
                            layer.putpixel((nX, nY), image.getpixel((x, y)))  
                            
                        #layer.putpixel((x, y), image.getpixel((x, y)))    
                        
            imageLayers.append(layer)

        return imageLayers  

    def apply_perspective_transformation(self, image_pil, depth_map_pil, tx, ty, zoom, num_layers, Fill):
        
        # Convert PIL images to NumPy arrays
        image = np.array(image_pil)
        depth_map = np.array(depth_map_pil)
        parallax_factor = 1
        if num_layers < 1:
            raise ValueError("Layers Count must be > 1.")

        # Créer un tableau vide pour stocker les couches
        layers = []

        # Calculer la plage de profondeur
        min_depth = np.min(depth_map)
        max_depth = np.max(depth_map)
        depth_range = max_depth - min_depth
        
        # Create an alpha channel (example)
        alpha_channel = np.full((image.shape[0], image.shape[1]), 255, dtype=np.uint8)
        # Create an empty RGBA image with the combined dimensions
        combined_image = np.dstack((image, alpha_channel))     
        
        # Get the size (width and height) of the target image
        width, height = image_pil.size
        imagesCombined = Image.new("RGBA", (width, height), (0, 0, 0, 0)) 

        # Créer les couches en fonction du nombre spécifié
        for i in range(num_layers):
            # Déterminer les valeurs de profondeur minimale et maximale pour cette couche
            layer_min_depth = min_depth + (i / num_layers) * depth_range
            layer_max_depth = min_depth + ((i + 1) / num_layers) * depth_range

            # Sélectionner les pixels de la depth map qui appartiennent à cette couche
            layer_mask = np.logical_and(depth_map >= layer_min_depth, depth_map <= layer_max_depth)
            if (Fill):           
                layer_mask = depth_map >= layer_min_depth
                
            image_rgb = image[:, :, :3]
            layer_alpha = (layer_mask[:, :, 0] * 255).astype(np.uint8)

            
            # Create an RGBA image by stacking the RGB channels with the alpha channel
            layer_rgba = np.dstack((image_rgb, layer_alpha))
 
            #layer_rgba = self.edge_padding(layer_rgba, 20)


            # Calculate the parallax_factor for this layer
            parallax_factor = i / (num_layers - 1)

            # Calculate the translation for this layer
            tx_offset = int(tx * parallax_factor)
            ty_offset = int(ty * parallax_factor)
        
            translated_mask = self.translate_layer(layer_rgba,tx_offset,ty_offset)

            z = i*zoom/num_layers + 1
            translated_mask = self.cv2_clipped_zoom(translated_mask, z)
            

            layer_image = Image.fromarray(translated_mask)
            layers.append(layer_image)

            # Replace visible pixels of image1 with corresponding pixels from image2
            imagesCombined.paste(layer_image, (0, 0), layer_image)


        return layers, imagesCombined
 


    def parallax_zoom(self, image, depth_map):
        # Convertir les images PIL en tableaux NumPy
        image_array = np.array(image)
        depth_map_array = np.array(depth_map)
        depth_map_array = depth_map_array[:, :, 0]
        radius = 5
        # Normaliser la carte de profondeur entre 0 et 1
        normalized_depth_map = depth_map_array.astype(float) / 255.0

        # Calculer le centre de l'image pour l'utiliser comme point de référence
        center_x, center_y = image.width // 2, image.height // 2

        # Créer une grille de coordonnées pour l'image
        y_coords, x_coords = np.mgrid[0:image.height, 0:image.width]

        # Calculer les distances par rapport au centre de l'image
        distances = np.sqrt((x_coords - center_x)**2 + (y_coords - center_y)**2)

        # Agrandir les pixels en fonction de la carte de profondeur
        scaled_distances = distances + (normalized_depth_map * radius)

        # Interpoler les nouvelles positions des pixels
        new_x_coords = ((x_coords - center_x) * (scaled_distances / distances)) + center_x
        new_y_coords = ((y_coords - center_y) * (scaled_distances / distances)) + center_y

        # Limiter les valeurs pour éviter les débordements
        new_x_coords = np.clip(new_x_coords, 0, image.width - 1)
        new_y_coords = np.clip(new_y_coords, 0, image.height - 1)

        # Interpoler les valeurs des pixels pour obtenir la nouvelle image
        new_image = np.zeros_like(image_array)
        for i in range(image.height):
            for j in range(image.width):
                new_image[i, j] = image_array[new_y_coords[i, j].astype(int), new_x_coords[i, j].astype(int)]

        # Convertir le tableau NumPy en image PIL
        new_image_pil = Image.fromarray(new_image.astype(np.uint8))

        return new_image_pil






    

    def cv2_clipped_zoom(self, img, zoom_factor=0):

        """
        Center zoom in/out of the given image and returning an enlarged/shrinked view of 
        the image without changing dimensions
        ------
        Args:
            img : ndarray
                Image array
            zoom_factor : float
                amount of zoom as a ratio [0 to Inf). Default 0.
        ------
        Returns:
            result: ndarray
               numpy ndarray of the same shape of the input img zoomed by the specified factor.          
        """
        if zoom_factor == 0:
            return img


        height, width = img.shape[:2] # It's also the final desired shape
        new_height, new_width = int(height * zoom_factor), int(width * zoom_factor)
    
        ### Crop only the part that will remain in the result (more efficient)
        # Centered bbox of the final desired size in resized (larger/smaller) image coordinates
        y1, x1 = max(0, new_height - height) // 2, max(0, new_width - width) // 2
        y2, x2 = y1 + height, x1 + width
        bbox = np.array([y1,x1,y2,x2])
        # Map back to original image coordinates
        bbox = (bbox / zoom_factor).astype(np.int32)
        y1, x1, y2, x2 = bbox
        cropped_img = img[y1:y2, x1:x2]
    
        # Handle padding when downscaling
        resize_height, resize_width = min(new_height, height), min(new_width, width)
        pad_height1, pad_width1 = (height - resize_height) // 2, (width - resize_width) //2
        pad_height2, pad_width2 = (height - resize_height) - pad_height1, (width - resize_width) - pad_width1
        pad_spec = [(pad_height1, pad_height2), (pad_width1, pad_width2)] + [(0,0)] * (img.ndim - 2)
    
        result = cv2.resize(cropped_img, (resize_width, resize_height))
        result = np.pad(result, pad_spec, mode='constant')
        assert result.shape[0] == height and result.shape[1] == width
        return result



    def translate_layer(self, layer_rgba, tx_offset, ty_offset):


        # Determine the new dimensions of the translated image
        new_height = layer_rgba.shape[0]
        new_width = layer_rgba.shape[1]

        # Create an empty image with the same shape as merged_image
        translated_mask = np.zeros_like(layer_rgba)

        # Calculate the cropping box
        x1, x2 = max(0, -tx_offset), min(new_width, new_width - tx_offset)
        y1, y2 = max(0, -ty_offset), min(new_height, new_height - ty_offset)

        # Calculate the region to copy from the original image
        src_x1, src_x2 = max(0, tx_offset), min(new_width, new_width + tx_offset)
        src_y1, src_y2 = max(0, ty_offset), min(new_height, new_height + ty_offset)

        # Copy the pixels from the original image to the translated image
        translated_mask[y1:y2, x1:x2] = layer_rgba[src_y1:src_y2, src_x1:src_x2]

        return translated_mask

    def edge_padding(self, image, padding_size):
        height, width, channels = image.shape

        # Extraction du canal alpha pour déterminer les bords
        alpha_channel = image[:, :, 3]

        # Création d'un masque autour du contour alpha
        alpha_mask = np.zeros((height, width), dtype=np.uint8)
        alpha_mask[alpha_channel < 255] = 1  # Si le pixel n'est pas complètement opaque (alpha < 255), c'est un bord

        # Dilatation du masque pour ajouter du padding
        kernel = np.ones((padding_size, padding_size), dtype=np.uint8)
        dilated_mask = cv2.dilate(alpha_mask, kernel, iterations=1)

        # Création d'une copie de l'image avec le padding
        padded_image = np.copy(image)

        for c in range(channels):  # Appliquer le padding pour chaque canal de couleur
            padded_image[:, :, c][dilated_mask == 1] = 0  # Mettre à zéro les pixels du bord

        return padded_image



    def clampPx(self, value):      
        return max(0, min(value, 255))

 
        
        
    def add_noise_with_mask(self, image, mask, strength):
        # Convert the input image and mask to NumPy arrays
        image_array = np.array(image)
        mask_array = np.array(mask)

        # Generate random noise with the same shape as the image
        noise = np.random.normal(scale=strength, size=image_array.shape)

        # Apply the mask to the noise
        noise *= mask_array

        # Add the noise to the image
        noisy_image_array = image_array + noise

        # Clip the pixel values to the valid range (0-255)
        noisy_image_array = np.clip(noisy_image_array, 0, 255).astype(np.uint8)

        # Convert the NumPy array back to an image
        noisy_image = Image.fromarray(noisy_image_array)

        return noisy_image
        
        
        
        
NODE_CLASS_MAPPINGS = {
        "Color correction": Color_Correction,
        "Displace Images with Mask": Displace_Image,
        "Add Noise to Image with Mask": AddNoiseToImageWithMask,
        "Displace Image with Depth": DisplaceImageWithDepth,
        "Zoom Image with Depth": ZoomWithDepth,
}
