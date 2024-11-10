#Code inspired by sv-nodes, thanks to him.

import comfy.samplers

class EssentialParams:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "cfg": ("FLOAT", {"min": 0, "max": 20, "step": 0.1, "default": 1.0}),
                "steps": ("INT", {"min": 1, "max": 100, "step": 1, "default": 20}),
                "sampler": (comfy.samplers.SAMPLER_NAMES,),
                "scheduler": (comfy.samplers.SCHEDULER_NAMES + ["ays"],),
                "denoise": ("FLOAT", {"min": 0, "max": 1, "step": 0.1, "default": 1.0})
            }
        }
    
    RETURN_TYPES = ("EParams",)
    RETURN_NAMES = ("_",)
    
    FUNCTION = "run"
    CATEGORY = "Fictiverse/Params"
    
    def run(self, cfg, steps, denoise, sampler, scheduler):
        if not isinstance(cfg, float) and not isinstance(cfg, int):
            raise TypeError("Invalid cfg input type")
        if not isinstance(steps, int):
            raise TypeError("Invalid steps input type")
        if not isinstance(denoise, float) and not isinstance(denoise, int):
            raise TypeError("Invalid denoise input type")
        if not isinstance(sampler, str):
            raise TypeError("Invalid sampler input type")
        return ((cfg, steps, denoise, sampler, scheduler, scheduler == "ays"),)

NODE_CLASS_MAPPINGS = {
    "Essential Params": EssentialParams,
}

NODE_CLASS_MAPPINGS["Essential Params"] = EssentialParams

class EssentialParamsExpand:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "_": ("EParams",)
            }
        }
    
    RETURN_TYPES = ("FLOAT", "INT", "FLOAT", comfy.samplers.SAMPLER_NAMES, comfy.samplers.SCHEDULER_NAMES, "BOOLEAN", "SAMPLER")
    RETURN_NAMES = ("cfg", "steps", "denoise", "sampler", "scheduler", "ays", "SAMPLER")
    
    FUNCTION = "run"
    CATEGORY = "Fictiverse/Params"
    
    def run(self, _):
        if not isinstance(_, tuple):
            raise TypeError("Invalid packet input type")
        if len(_) != 6:
            raise ValueError("Invalid packet length")
        cfg = _[0] or 8.0
        steps = _[1] or 10
        denoise = _[2] or 1.0
        sampler = _[3] or comfy.samplers.SAMPLER_NAMES[0]
        sampler2 = comfy.samplers.sampler_object(sampler)
        scheduler = comfy.samplers.SCHEDULER_NAMES[0] if _[4] in [None, "ays"] else _[4]
        ays = _[5] or False
        return cfg, steps, denoise, sampler, scheduler, ays, sampler2

NODE_CLASS_MAPPINGS["Essential Params Expand"] = EssentialParamsExpand