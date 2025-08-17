class PromptAssembler:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "pre_strength": ("FLOAT", {"default": 1.0}),
                "pre_prompt": ("STRING", {"default": ""}),
                "main_strength": ("FLOAT", {"default": 1.0}),
                "main_prompt": ("STRING", {"default": ""}),
                "post_strength": ("FLOAT", {"default": 1.0}),
                "post_prompt": ("STRING", {"default": ""}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("prompt",)
    FUNCTION = "assemble_prompt"
    CATEGORY = "Fictiverse"

    def assemble_prompt(self, pre_strength, pre_prompt, main_strength, main_prompt, post_strength, post_prompt):
        parts = []

        def format_prompt(prompt, strength):
            if not prompt or not prompt.strip():
                return []  # ignore empty prompts
            lines = [line for line in prompt.splitlines() if line.strip()]
            result = []
            for line in lines:
                clean = line.strip()
                if strength == 1.0:
                    result.append(clean)
                else:
                    result.append(f"({clean}:{strength:.2f})")
            return result

        for prompt, strength in [
            (pre_prompt, pre_strength),
            (main_prompt, main_strength),
            (post_prompt, post_strength),
        ]:
            parts.extend(format_prompt(prompt, strength))

        # Join all non-empty parts with commas
        return (", ".join(parts),)


# Register the node
NODE_CLASS_MAPPINGS = {
    "Prompt Assembler": PromptAssembler
}
