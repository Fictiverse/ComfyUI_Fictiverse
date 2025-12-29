import re

class FV_CleanStyleFromCaption:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "caption": ("STRING", {"default": ""}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("clean_caption",)
    FUNCTION = "clean_caption"
    CATEGORY = "Fictiverse/Text"

    def clean_caption(self, caption):
        if not caption or not caption.strip():
            return ("",)

        text = caption.strip()

        # --------------------------------------------------
        # 1. Remove generic caption starters
        # --------------------------------------------------
        text = re.sub(
            r"^(the image (shows|is)|this image (shows|is))\s+",
            "",
            text,
            flags=re.IGNORECASE
        )

        # --------------------------------------------------
        # 2. Remove leading style blocks ending with "of"
        #    (article optional)
        # --------------------------------------------------
        text = re.sub(
            r"""
            ^
            (?:[\w\-]+\s+)*              # any style words (anime-style, digital, etc.)
            (?:a|an)?\s*                 # optional article
            (drawing|illustration|painting|rendering|
             render|model|photo|photograph|
             image|scene)
            \s+
            of
            \s+
            """,
            "",
            text,
            flags=re.IGNORECASE | re.VERBOSE
        )

        # --------------------------------------------------
        # 3. Cleanup leftover junk (",", "a ,", etc.)
        # --------------------------------------------------
        text = re.sub(r"\ba\s*,", "", text, flags=re.IGNORECASE)
        text = re.sub(r"\s{2,}", " ", text)
        text = re.sub(r"\s*,\s*", ", ", text)
        text = text.strip(" ,")

        return (text.strip(),)


NODE_CLASS_MAPPINGS = {
    "Clean Style From Caption": FV_CleanStyleFromCaption
}
