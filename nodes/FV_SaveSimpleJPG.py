import numpy as np
from PIL import Image
import folder_paths
import os

class Save_as_jpg:
    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()
        self.type = "output"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "filename_prefix": ("STRING", {"default": "ComfyUI"}),
                "compression": ("INT", {"default": 80, "min": 10, "max": 100, "step": 1}),
            }
        }

    RETURN_TYPES = ()
    FUNCTION = "Save_as_jpg"
    OUTPUT_NODE = True
    CATEGORY = "Fictiverse"

    def Save_as_jpg(self, images, filename_prefix="ComfyUI", compression=80):
        def map_filename(filename):
            prefix_len = len(os.path.basename(filename_prefix))
            prefix = filename[:prefix_len + 1]
            try:
                digits = int(filename[prefix_len + 1:].split('_')[0])
            except:
                digits = 0
            return (digits, prefix)

        def compute_vars(input):
            input = input.replace("%width%", str(images[0].shape[1]))
            input = input.replace("%height%", str(images[0].shape[0]))
            return input

        filename_prefix = compute_vars(filename_prefix)

        subfolder = os.path.dirname(os.path.normpath(filename_prefix))
        filename = os.path.basename(os.path.normpath(filename_prefix))

        full_output_folder = os.path.join(self.output_dir, subfolder)

        if os.path.commonpath((self.output_dir, os.path.abspath(full_output_folder))) != self.output_dir:
            print("Saving image outside the output folder is not allowed.")
            return {}

        try:
            counter = max(
                filter(
                    lambda a: a[1][:-1] == filename and a[1][-1] == "_",
                    map(map_filename, os.listdir(full_output_folder))
                )
            )[0] + 1
        except ValueError:
            counter = 1
        except FileNotFoundError:
            os.makedirs(full_output_folder, exist_ok=True)
            counter = 1

        results = list()

        for image in images:
            i = 255.0 * image.cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))

            file = f"{filename}_{counter:05}_.jpg"

            img.save(
                os.path.join(full_output_folder, file),
                quality=compression
            )

            results.append({
                "filename": file,
                "subfolder": subfolder,
                "type": self.type
            })

            counter += 1

        return {"ui": {"images": results}}


NODE_CLASS_MAPPINGS = {
    "Save_as_jpg": Save_as_jpg
}