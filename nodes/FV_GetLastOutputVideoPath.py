import os
import glob
from pathlib import Path

class GetLastOutputVideoPath:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "subfolder": ("STRING", {"default": ""}),  
                "sort_by": (["Date", "Name"], {"default": "Date"}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("video_path",)
    FUNCTION = "get_last_video"
    CATEGORY = "Fictiverse"

    def IS_CHANGED(s):
        return float("NaN")

    def get_last_video(self, subfolder, sort_by,):

        # Root directory of ComfyUI (3 levels up from this file)
        comfy_dir = Path(__file__).resolve().parents[3]
        base_dir = comfy_dir / "output" / subfolder

        if not os.path.exists(base_dir):
            return ("",)  # Return empty string if the folder does not exist

        # Search for .webp and .mp4 files
        files = glob.glob(os.path.join(base_dir, "*.webp")) + glob.glob(os.path.join(base_dir, "*.mp4"))
        if not files:
            return ("",)  # Return empty string if no matching files are found

        if sort_by == "Date":
            # Sort files by last modified time (newest first)
            files.sort(key=os.path.getmtime, reverse=True)
        else:
            # Sort files alphabetically by name (reverse order)
            files.sort(reverse=True)

        return (files[0],)  # Return the most recent or last file based on mode

# Register the node in ComfyUI
NODE_CLASS_MAPPINGS = {
    "Get Last Output Video Path": GetLastOutputVideoPath
}
