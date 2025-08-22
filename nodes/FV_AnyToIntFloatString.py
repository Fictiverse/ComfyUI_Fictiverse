# Hack: string type that is always equal in not equal comparisons
class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False

# notre wildcard pour tout type
any = AnyType("*")

class AnyToIntFloatString:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "value": (any,),  # accepte n'importe quel type
            }
        }

    RETURN_TYPES = ("INT", "FLOAT", "STRING")
    RETURN_NAMES = ("as_int", "as_float", "as_string")

    FUNCTION = "run"
    CATEGORY = "Fictiverse/Utils"

    def run(self, value):
        # conversion en int si possible
        try:
            int_val = int(value)
        except (ValueError, TypeError):
            int_val = 0

        # conversion en float si possible
        try:
            float_val = float(value)
        except (ValueError, TypeError):
            float_val = 0.0

        # conversion en string
        try:
            str_val = str(value)
        except Exception:
            str_val = ""

        return (int_val, float_val, str_val)


NODE_CLASS_MAPPINGS = {
    "Any to Int/Float/String": AnyToIntFloatString,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Any to Int/Float/String": "Any to Int/Float/String",
}
