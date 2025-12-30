import nodes
import folder_paths

class FV_LoRA_Enable_With_Prefix:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model": ("MODEL",),
                "clip": ("CLIP",),
                "enable": ("BOOLEAN", {"default": True}),
                "lora_name": (folder_paths.get_filename_list("loras"),),
                "strength_model": ("FLOAT", {
                    "default": 1.0,
                    "min": -5.0,
                    "max": 5.0,
                    "step": 0.05
                }),
                "strength_clip": ("FLOAT", {
                    "default": 1.0,
                    "min": -5.0,
                    "max": 5.0,
                    "step": 0.05
                }),
                "text": ("STRING", {
                    "default": "",
                    "multiline": True
                }),
                # socket-only, comme Klinter
                "prefix": ("STRING", {
                    "forceInput": True
                }),
            }
        }

    RETURN_TYPES = ("MODEL", "CLIP", "STRING")
    RETURN_NAMES = ("model", "clip", "text")
    FUNCTION = "apply"
    CATEGORY = "Fictiverse/LoRA"

    def apply(
        self,
        model,
        clip,
        enable,
        lora_name,
        strength_model,
        strength_clip,
        text,
        prefix
    ):
        # --------------------------------------------------
        # Normalize inputs
        # --------------------------------------------------
        prefix = (prefix or "").strip()
        text = (text or "").strip()

        # --------------------------------------------------
        # TEXT LOGIC (authoritative)
        # --------------------------------------------------
        if not enable:
            # LoRA OFF → prefix only
            final_text = prefix
        else:
            # LoRA ON → prefix + text (or prefix alone)
            if prefix and text:
                final_text = f"{prefix} {text}"
            else:
                final_text = prefix or text

        # --------------------------------------------------
        # Apply LoRA only if enabled
        # --------------------------------------------------
        if enable:
            lora_loader = nodes.LoraLoader()
            model, clip = lora_loader.load_lora(
                model,
                clip,
                lora_name,
                strength_model,
                strength_clip
            )

        return (model, clip, final_text)


NODE_CLASS_MAPPINGS = {
    "LoRA Enable With Prefix": FV_LoRA_Enable_With_Prefix
}
