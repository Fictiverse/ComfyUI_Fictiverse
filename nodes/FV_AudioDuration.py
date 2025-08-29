import torch

class AudioDuration:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "audio": ("AUDIO",),
            }
        }

    RETURN_TYPES = ("INT", "FLOAT")
    RETURN_NAMES = ("duration_ms", "duration_sec")
    FUNCTION = "run"
    CATEGORY = "Fictiverse/Audio"

    def run(self, audio):
        waveform = audio["waveform"]
        sample_rate = audio["sample_rate"]
        duration_ms = int((waveform.shape[-1] / sample_rate) * 1000)
        duration_sec = float(duration_ms) / 1000.0
        return (duration_ms, duration_sec)

NODE_CLASS_MAPPINGS = {
    "Audio Duration": AudioDuration,
}
