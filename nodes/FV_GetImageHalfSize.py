class FV_GetImageHalfSize:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
            }
        }

    RETURN_TYPES = ("INT", "INT")
    RETURN_NAMES = ("width", "height")
    FUNCTION = "run"
    CATEGORY = "Fictiverse/Resize"

    def run(self, image):
        # image est un batch : (batch, height, width, channels)
        first_image = image[0]

        height = first_image.shape[0]
        width = first_image.shape[1]

        if width >= height:
            width = width // 2
        else:
            height = height // 2

        return (width, height)


NODE_CLASS_MAPPINGS = {
    "FV Get Image Half Size": FV_GetImageHalfSize
}
