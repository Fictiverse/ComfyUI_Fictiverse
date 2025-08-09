#Code inspired by sv-nodes, thanks to him.

import math

class VideoParams:
    RATIOS = ["1:1", "5:4", "4:3", "3:2", "16:9", "21:9"]
    
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "base": ("INT", {"default": 768, "min": 128, "max": 4096, "step": 128}),
                "ratio": (VideoParams.RATIOS,),
                "orientation": ("BOOLEAN", {"default": False, "label_on": "Portrait ▯", "label_off": "Landscape ▭"}),
                "Frames": ("INT", {"min": 1, "max": 600, "step": 1, "default": 81}),
                "FPS": ("INT", {"min": 1, "max": 120, "step": 1, "default": 16})
            }
        }
    
    RETURN_TYPES = ("VParams",)
    RETURN_NAMES = ("_",)
    
    FUNCTION = "run"
    CATEGORY = "Fictiverse/Params"
    
    def run(self, base, ratio, orientation, Frames, FPS,):
        
        ratio = ratio.split(":")
        if len(ratio) != 2:
            raise ValueError("Invalid ratio")
        
        ratio = math.sqrt(float(ratio[0]) / float(ratio[1]))
        
        width = math.floor(base * ratio / 64) * 64 
        height = math.floor(base / ratio / 64) * 64 
        
        #Frames = max(7, (math.floor(Frames / 6) * 6) + 1) 
        megapixels = (base*base)/1000000



        if orientation:
            width, height = height, width
        return ((width, height, Frames, float(FPS), megapixels),)

NODE_CLASS_MAPPINGS = {
    "Video Params": VideoParams,
}

class VideoParamsExpand:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "_": ("VParams",)
            }
        }

    RETURN_TYPES = ("INT", "INT", "INT", "FLOAT", "FLOAT")
    RETURN_NAMES = ("width", "height", "frames", "fps", "Megapixels")
    
    FUNCTION = "run"
    CATEGORY = "Fictiverse/Params"
    
    def run(self, _):
        if not isinstance(_, tuple):
            raise TypeError("Invalid packet input type")
        if len(_) != 5:
            raise ValueError("Invalid packet length")
        return _

NODE_CLASS_MAPPINGS["Video Params Expand"] = VideoParamsExpand