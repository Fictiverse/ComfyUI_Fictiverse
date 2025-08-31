import torch

class WaveformDevice:
    """
    Convertit un AUDIO (dict contenant waveform et sample_rate)
    entre CPU et GPU selon le booléen 'to_gpu'.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "audio": ("AUDIO",),  # Entrée AUDIO complète
                "switch_to": ("BOOLEAN", {
                    "default": False,
                    "label_on": "GPU (CUDA) 🚀",
                    "label_off": "CPU 🖥️"
                }),
            }
        }

    RETURN_TYPES = ("AUDIO",)
    RETURN_NAMES = ("audio",)
    FUNCTION = "convert"
    CATEGORY = "Fictiverse/Audio"

    def convert(self, audio, switch_to):
        """
        Déplace le tenseur 'waveform' entre CPU et GPU.
        """
        if not isinstance(audio, dict) or "waveform" not in audio:
            raise TypeError("L'entrée 'audio' doit être un dict ComfyUI avec 'waveform' et 'sample_rate'")

        waveform = audio["waveform"]

        if not torch.is_tensor(waveform):
            raise TypeError("'waveform' doit être un tenseur PyTorch")

        # Choisir le device
        target_device = torch.device("cuda" if switch_to and torch.cuda.is_available() else "cpu")
        waveform = waveform.to(target_device)

        # Reconstruire l'objet AUDIO
        return ({
            "waveform": waveform,
            "sample_rate": audio.get("sample_rate", 44100)
        },)


NODE_CLASS_MAPPINGS = {
    "WaveformDevice": WaveformDevice
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "WaveformDevice": "Waveform Device Switch"
}
