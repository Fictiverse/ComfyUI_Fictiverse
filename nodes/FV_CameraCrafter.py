# ---------------------------
# Node: Camera Settings
# ---------------------------
class FV_Camera_Settings:
    CAMERA_DESCRIPTIONS = {
        "None": "",
        "Orthographic 3-view": "Orthographic character sheet with 3 views, one side view, one front view, and one back view, neutral stance, consistent proportions across all views.",
        "Medium shot": "Three-quarter length medium shot, focusing on the character from waist up, neutral pose, balanced composition.",
        "Close-up": "Close-up shot of the character's face, highlighting expressions and facial details, neutral lighting.",
        "Long shot": "Full-body long shot showing the character in their environment, maintaining correct proportions and perspective.",
        "Bird's eye view": "Top-down bird's eye view of the character, showing layout and surroundings from above.",
        "Worm's eye view": "Low-angle worm's eye view looking up at the character, emphasizing height and power.",
        "Over-the-shoulder": "Over-the-shoulder shot showing the character from behind another character, perspective focused on interaction.",
        "First-person": "First-person perspective from the character's viewpoint, immersive and realistic.",
        "Panoramic": "Wide panoramic view capturing the character and surroundings in a broad context.",
        "Wide-angle": "Wide-angle shot exaggerating perspective and depth, character remains central focus.",
        "Telephoto": "Telephoto shot compressing distance, focusing tightly on the character from afar.",
        "Portrait": "Portrait-style framing with character centered, neutral background, emphasizing face and upper body.",
        "Landscape": "Landscape-style framing showing character in wide environment, emphasizing scenery and context."
    }

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "camera_type": (tuple(cls.CAMERA_DESCRIPTIONS.keys()),),
            },
            "optional": {
                "prefix": ("*", {}),
            }
        }
    
    @classmethod
    def VALIDATE_INPUTS(cls, input_types):
        return True

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("camera_text",)
    FUNCTION = "apply"
    CATEGORY = "Fictiverse/Camera"

    def apply(self, camera_type, prefix=""):
        description = self.CAMERA_DESCRIPTIONS.get(camera_type, "")
        if not description:
            return (prefix,)
        return (f"{prefix}{description}",)


# ---------------------------
# Node registration
# ---------------------------
NODE_CLASS_MAPPINGS = {
    "Camera Settings": FV_Camera_Settings,
}