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
                "base": ("INT", {"default": 768, "min": 64, "max": 4096, "step": 64}),
                "ratio": (VideoParams.RATIOS,),
                "orientation": ("BOOLEAN", {"default": False, "label_on": "Portrait ▯", "label_off": "Landscape ▭"}),
                "Frames": ("INT", {"min": 7, "max": 511, "step": 6, "default": 49}),
                "FPS": ("INT", {"min": 1, "max": 64, "step": 1, "default": 8})
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
        
        Frames = max(7, (math.floor(Frames / 6) * 6) + 1) 
        
        if orientation:
            width, height = height, width
        return ((width, height, Frames, FPS),)

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
    
    RETURN_TYPES = ("INT", "INT", "INT", "INT")
    RETURN_NAMES = ("width", "height", "frames", "fps")
    
    FUNCTION = "run"
    CATEGORY = "Fictiverse/Params"
    
    def run(self, _):
        if not isinstance(_, tuple):
            raise TypeError("Invalid packet input type")
        if len(_) != 4:
            raise ValueError("Invalid packet length")
        return _

NODE_CLASS_MAPPINGS["Video Params Expand"] = VideoParamsExpand