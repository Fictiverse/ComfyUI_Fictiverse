import nodes
import folder_paths

class FV_Text_Enable_With_Prefix:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "enable": ("BOOLEAN", {"default": True}),
                "text": ("STRING", {
                    "default": "",
                    "multiline": True
                }),
                # socket-only pour forcer l'entrée de prefix
                "prefix": ("STRING", {
                    "forceInput": True
                }),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "apply"
    CATEGORY = "Fictiverse/Text"

    def apply(
        self,
        enable,
        text,
        prefix
    ):
        # --------------------------------------------------
        # Normalisation des entrées
        # --------------------------------------------------
        prefix = (prefix or "").strip()
        text = (text or "").strip()

        # --------------------------------------------------
        # Logique texte
        # --------------------------------------------------
        if not enable:
            # Bypass → prefix seul
            final_text = prefix
        else:
            # Activation → prefix + texte (ou texte seul si prefix vide)
            if prefix and text:
                final_text = f"{prefix} {text}"
            else:
                final_text = prefix or text

        return (final_text,)


NODE_CLASS_MAPPINGS = {
    "Text Enable With Prefix": FV_Text_Enable_With_Prefix
}
