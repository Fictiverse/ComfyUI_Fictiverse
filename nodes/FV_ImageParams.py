#Code inspired by sv-nodes, thanks to him.

import math


class ImageParams:
    RATIOS = ["1:1", "5:4", "4:3", "3:2", "16:9", "2:1", "21:9", "32:9"]
    
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "base": ("INT", {"default": 768, "min": 64, "max": 4096, "step": 64}),
                "ratio": (ImageParams.RATIOS,),
                "orientation": ("BOOLEAN", {"default": False, "label_on": "Portrait ▯", "label_off": "Landscape ▭"}),
                "hires": ("FLOAT", {"min": 1, "max": 4, "step": 0.25, "default": 1.5}),
                "batch": ("INT", {"min": 1, "max": 64, "step": 1, "default": 1})
            }
        }
    
    RETURN_TYPES = ("IParams",)
    RETURN_NAMES = ("_",)
    
    FUNCTION = "run"
    CATEGORY = "Fictiverse/Params"
    
    def run(self, base, ratio, orientation, hires, batch,):
        
        ratio = ratio.split(":")
        if len(ratio) != 2:
            raise ValueError("Invalid ratio")
        
        ratio = math.sqrt(float(ratio[0]) / float(ratio[1]))
        
        width = math.floor(base * ratio / 64) * 64 
        height = math.floor(base / ratio / 64) * 64
        
        if orientation:
            width, height = height, width
        return ((width, height, hires, batch),)

NODE_CLASS_MAPPINGS = {
    "Image Params": ImageParams,
}


class ImageParamsExpand:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "_": ("IParams",)
            }
        }
    
    RETURN_TYPES = ("INT", "INT", "FLOAT", "INT")
    RETURN_NAMES = ("width", "height", "hires ratio", "batch size")
    
    FUNCTION = "run"
    CATEGORY = "Fictiverse/Params"
    
    def run(self, _):
        if not isinstance(_, tuple):
            raise TypeError("Invalid packet input type")
        if len(_) != 4:
            raise ValueError("Invalid packet length")
        return _

NODE_CLASS_MAPPINGS["Image Params Expand"] = ImageParamsExpand