import math

# ==========================================
# CLASSSES PARAMS VIDÉO
# ==========================================


class VideoParams:
    RATIOS = ["1:1", "5:4", "4:3", "3:2", "16:9", "21:9"]

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "base": (
                    "INT",
                    {"default": 768, "min": 128, "max": 4096, "step": 128},
                ),
                "ratio": (cls.RATIOS,),
                "orientation": ("BOOLEAN", {"default": False, "label_on": "Portrait ▯", "label_off": "Landscape ▭"}),
                "duration": (
                    "FLOAT",
                    {"default": 10.0, "min": 1.0, "max": 60.0, "step": 1.0},
                ),
            }
        }

    RETURN_TYPES = ("VParams",)
    RETURN_NAMES = ("_",)
    FUNCTION = "run"
    CATEGORY = "Fictiverse/Params"

    def run(self, base, ratio, orientation, duration):
        ratio_parts = ratio.split(":")
        if len(ratio_parts) != 2:
            raise ValueError("Invalid ratio format")

        ratio_val = math.sqrt(float(ratio_parts[0]) / float(ratio_parts[1]))

        # Calcul des dimensions multiples de 32
        width = math.floor(base * ratio_val / 32) * 32
        height = math.floor(base / ratio_val / 32) * 32

        if orientation:
            width, height = height, width

        # Calcul plus précis des mégapixels réels en sortie
        megapixels = (width * height) / 1_000_000.0

        return ((width, height, duration, megapixels),)


class VideoParamsExpand:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"_": ("VParams",)}}

    RETURN_TYPES = ("INT", "INT", "FLOAT", "FLOAT")
    RETURN_NAMES = ("width", "height", "duration", "Megapixels")
    FUNCTION = "run"
    CATEGORY = "Fictiverse/Params"

    def run(self, _):
        if not isinstance(_, (tuple, list)):
            raise TypeError("Invalid packet input type")
        if len(_) != 4:
            raise ValueError(
                f"Invalid packet length (expected 4, got {len(_)})"
            )
        return _


# ==========================================
# NOUVEAU NODE : DURATION TO FRAMES
# ==========================================


class DurationToFrames:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "duration": (
                    "FLOAT",
                    {"default": 10.0, "min": 0.1, "max": 1000.0, "step": 0.1},
                ),
                "fps": (
                    "INT",
                    {"default": 24, "min": 1, "max": 240, "step": 1},
                ),
            }
        }

    RETURN_TYPES = ("INT", "FLOAT")
    RETURN_NAMES = ("int", "float")
    FUNCTION = "run"
    CATEGORY = "Fictiverse/Params"

    def run(self, duration, fps):
        # Traduction de l'expression :
        # a -> duration
        # 24 -> fps
        raw_frames = max(5, round(duration * fps))
        frame_count = raw_frames + (5 - (raw_frames % 17)) % 17

        return (frame_count, float(frame_count))


# ==========================================
# MAPPINGS COMFYUI
# ==========================================
NODE_CLASS_MAPPINGS = {
    "Video Params": VideoParams,
    "Video Params Expand": VideoParamsExpand,
    "Duration To Frames": DurationToFrames,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Video Params": "Video Params",
    "Video Params Expand": "Video Params Expand",
    "Duration To Frames": "Duration To Frames",
}