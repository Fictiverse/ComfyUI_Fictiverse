import nodes

# ---------------------------
# Node: Character Appearance
# ---------------------------
class FV_Character_Appearance:
    GENDERS = ["None", "Male", "Female"]
    BODY_TYPES = ["None", "Skinny", "Slim", "Athletic", "Muscular", "Curvy", "Heavy", "Very fat"]
    HEIGHTS = ["None", "Small", "Tall", "Gigantic"]
    SKIN_TONES = ["None", "Pale", "Fair", "Olive", "Dark"]
    HAIR_STYLES = ["None", "Short", "Long", "Curly", "Bald"]
    HAIR_COLORS = ["None", "Black", "Brown", "Blonde", "Red", "Gray", "Blue", "Green", "Purple", "White"]
    EYE_COLORS = ["None", "Blue", "Green", "Brown", "Hazel"]

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "gender": (cls.GENDERS,),
                "body_type": (cls.BODY_TYPES,),
                "height": (cls.HEIGHTS,),
                "skin_tone": (cls.SKIN_TONES,),
                "hair_style": (cls.HAIR_STYLES,),
                "hair_color": (cls.HAIR_COLORS,),
                "eye_color": (cls.EYE_COLORS,),
            },
            "optional": {
                "prefix": ("*", {}),
            }
        }
    
    @classmethod
    def VALIDATE_INPUTS(cls, input_types):
        return True  # Permet de bypasser la validation du type

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("appearance_text",)
    FUNCTION = "apply"
    CATEGORY = "Fictiverse/Character"

    def apply(self, gender, body_type, height, skin_tone, hair_style, hair_color, eye_color, prefix=""):
        gender_txt = "person" if gender == "None" else gender.lower()

        parts = []
        if body_type != "None":
            parts.append(body_type.lower())
        if height != "None":
            parts.append(height.lower())
        if skin_tone != "None":
            parts.append(skin_tone.lower() + " skin")
        parts.append(gender_txt)
        text = "A " + " ".join(parts)

        eye_text = None
        if eye_color != "None":
            eye_text = f"{eye_color.lower()} eyes"

        hair_parts = []
        if hair_color != "None":
            hair_parts.append(hair_color.lower())
        if hair_style != "None":
            hair_parts.append(hair_style.lower())

        hair_text = None
        if hair_parts:
            if len(hair_parts) == 1:
                hair_text = f"{hair_parts[0]} hair"
            else:
                hair_text = f"{' '.join(hair_parts)} haircut"

        extras = []
        if eye_text:
            extras.append(eye_text)
        if hair_text:
            extras.append(hair_text)
        if extras:
            text += " with " + " and ".join(extras)

        text += "."
        return (f"{prefix}{text}",)


# ---------------------------
# Node: Character Makeup
# ---------------------------
class FV_Character_Makeup:
    MAKEUP_STYLES = ["None", "Natural", "Glam", "Theatrical"]
    FOUNDATIONS = ["None", "Light", "Medium", "Dark"]
    BLUSHES = ["None", "Pink", "Peach", "Bronze"]
    EYESHADOWS = ["None", "Neutral", "Smoky", "Colorful"]
    EYELINERS = ["None", "Winged", "Smudged", "Cat-eye"]
    MASCARA = ["None", "True", "False"]
    LIPSTICKS = ["None", "Red", "Pink", "Nude", "Dark"]

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "makeup_style": (cls.MAKEUP_STYLES,),
                "foundation": (cls.FOUNDATIONS,),
                "blush": (cls.BLUSHES,),
                "eyeshadow": (cls.EYESHADOWS,),
                "eyeliner": (cls.EYELINERS,),
                "mascara": (cls.MASCARA,),
                "lipstick": (cls.LIPSTICKS,),
            },
            "optional": {
                "prefix": ("*", {}),
            }
        }
    
    @classmethod
    def VALIDATE_INPUTS(cls, input_types):
        return True  # Permet de bypasser la validation du type

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("makeup_text",)
    FUNCTION = "apply"
    CATEGORY = "Fictiverse/Character"

    def apply(self, makeup_style, foundation, blush, eyeshadow, eyeliner, mascara, lipstick, prefix=""):
        parts = []

        if makeup_style != "None":
            parts.append(makeup_style.lower())
        if foundation != "None":
            parts.append(f"{foundation.lower()} foundation")
        if blush != "None":
            parts.append(f"{blush.lower()} blush")
        if eyeshadow != "None":
            parts.append(f"{eyeshadow.lower()} eyeshadow")
        if eyeliner != "None":
            parts.append(f"{eyeliner.lower()} eyeliner")
        if mascara == "True":
            parts.append("mascara")
        elif mascara == "False":
            parts.append("no mascara")
        if lipstick != "None":
            parts.append(f"{lipstick.lower()} lipstick")

        if not parts:
            return (prefix,)

        if len(parts) == 1:
            text = f"makeup with {parts[0]}"
        else:
            text = "makeup with " + ", ".join(parts[:-1]) + " and " + parts[-1]

        text += "."
        return (f"{prefix}{text}",)



# ---------------------------
# Node: Character Clothing
# ---------------------------
class FV_Character_Clothing:
    TOPS = ["None", "No", "Shirt", "Blouse", "Jacket", "Coat", "Sweater", "Hoodie"]
    BOTTOMS = ["None", "No", "Pants", "Skirt", "Shorts", "Leggings"]
    FULL_BODY = ["None", "No", "Dress", "Suit", "Armor"]
    COLORS = ["None", "Red", "Blue", "Green", "Black", "White"]
    ACCESSORIES = ["None", "Belt", "Necklace", "Ring", "Hat"]

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "top": (cls.TOPS,),
                "top_color": (cls.COLORS,),
                "bottom": (cls.BOTTOMS,),
                "bottom_color": (cls.COLORS,),
                "full_body": (cls.FULL_BODY,),
                "full_body_color": (cls.COLORS,),
                "accessories": (cls.ACCESSORIES,),
            },
            "optional": {
                "prefix": ("*", {}),
            }
        }
    
    @classmethod
    def VALIDATE_INPUTS(cls, input_types):
        return True  # Permet de bypasser la validation du type

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("clothing_text",)
    FUNCTION = "apply"
    CATEGORY = "Fictiverse/Character"

    def apply(self, top, top_color, bottom, bottom_color, full_body, full_body_color, accessories, prefix=""):
        parts = []

        if full_body != "None":
            if full_body == "No":
                parts.append("nothing and is naked")
            else:
                fb_part = full_body.lower()
                if full_body_color != "None":
                    fb_part += f" in {full_body_color.lower()}"
                parts.append(fb_part)
        else:
            if top != "None":
                if top == "No":
                    parts.append("nothing on top")
                else:
                    t_part = top.lower()
                    if top_color != "None":
                        t_part += f" in {top_color.lower()}"
                    parts.append(t_part)
            if bottom != "None":
                if bottom == "No":
                    parts.append("nothing on bottom")
                else:
                    b_part = bottom.lower()
                    if bottom_color != "None":
                        b_part += f" in {bottom_color.lower()}"
                    parts.append(b_part)

        if accessories != "None":
            parts.append(f"with {accessories.lower()}")

        if not parts:
            return (prefix,)

        if len(parts) == 1:
            text = f"wearing {parts[0]}"
        else:
            text = "wearing " + ", ".join(parts[:-1]) + " and " + parts[-1]

        text += "."
        return (f"{prefix}{text}",)



# ---------------------------
# Node: Character Expressions
# ---------------------------
class FV_Character_Expressions:
    EXPRESSIONS = [
        "happy",
        "sad",
        "angry",
        "surprised",
        "confused",
        "tired",
        "smiling",
        "frowning",
        "winking",
        "terrified",
        "shocked",
        "panicked",
        "nervous",
        "excited",
        "bored",
        "disgusted",
        "anxious",
        "relieved"
    ]

    @classmethod
    def INPUT_TYPES(cls):
        # Chaque expression est un booléen, plus un prefix wildcard
        required = {expr: ("BOOLEAN",) for expr in cls.EXPRESSIONS}
        optional = {
            "prefix": ("*", {})  # Champ texte libre pour préfix
        }
        return {
            "required": required,
            "optional": optional,
        }

    @classmethod
    def VALIDATE_INPUTS(cls, input_types):
        return True

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("expression_text",)
    FUNCTION = "apply"
    CATEGORY = "Fictiverse/Character"

    def apply(
        self,
        happy=False,
        sad=False,
        angry=False,
        surprised=False,
        confused=False,
        tired=False,
        smiling=False,
        frowning=False,
        winking=False,
        terrified=False,
        shocked=False,
        panicked=False,
        nervous=False,
        excited=False,
        bored=False,
        disgusted=False,
        anxious=False,
        relieved=False,
        prefix=None,
    ):
        if prefix is None:
            prefix = ""

        # Accumuler les expressions activées
        active_expressions = []
        for expr_name in self.EXPRESSIONS:
            if locals()[expr_name]:
                active_expressions.append(expr_name)

        if not active_expressions:
            return (prefix,)

        # Construire la phrase finale
        if len(active_expressions) == 1:
            text = f"{active_expressions[0]} expression"
        else:
            text = f"{', '.join(active_expressions[:-1])} and {active_expressions[-1]} expressions"

        text += "."
        return (f"{prefix}{text}",)

    

# ---------------------------
# Node registration
# ---------------------------
NODE_CLASS_MAPPINGS = {
    "Character Appearance": FV_Character_Appearance,
    "Character Makeup": FV_Character_Makeup,
    "Character Clothing": FV_Character_Clothing,
    "Character Expressions": FV_Character_Expressions,
}
