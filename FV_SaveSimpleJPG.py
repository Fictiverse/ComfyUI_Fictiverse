import numpy as np
from PIL import Image
import folder_paths
import os

class SaveSimpleJPG:
    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()
        self.type = "output"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "filename_prefix": ("STRING", {"default": "ComfyUI"}),
                "quality": ("INT", {"default": 80, "min": 10, "max": 100, "step": 1}),
            }
        }

    RETURN_TYPES = ()
    FUNCTION = "save_jpg"
    OUTPUT_NODE = True
    CATEGORY = "Fictiverse"

    def save_jpg(self, images, filename_prefix="ComfyUI", quality=80):
        output_folder = self.output_dir
        os.makedirs(output_folder, exist_ok=True)

        results = []
        counter = 1

        for image in images:
            i = 255. * image.cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))

            filename = f"{filename_prefix}_{counter:05}.jpg"
            filepath = os.path.join(output_folder, filename)

            img.save(filepath, format="JPEG", quality=quality)

            results.append({
                "filename": filename,
                "subfolder": "",
                "type": self.type
            })

            counter += 1

        return {"ui": {"images": results}}


NODE_CLASS_MAPPINGS = {
    "Save Simple JPG": SaveSimpleJPG,
}