class MathOperation:
    OPERATIONS = ["+", "-", "*", "/", "^"]

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "A": ("FLOAT", {"default": 0.0}),
                "B": ("FLOAT", {"default": 0.0}),
                "operation": (s.OPERATIONS,),
            }
        }

    RETURN_TYPES = ("INT", "FLOAT")
    RETURN_NAMES = ("result_int", "result_float")

    FUNCTION = "run"
    CATEGORY = "Fictiverse/Math"

    def run(self, A, B, operation):
        if operation == "+":
            result = A + B
        elif operation == "-":
            result = A - B
        elif operation == "*":
            result = A * B
        elif operation == "/":
            if B == 0:
                raise ZeroDivisionError("Division by zero")
            result = A / B
        elif operation == "^":
            result = A ** B
        else:
            raise ValueError(f"Unknown operation {operation}")

        # On sort les deux types
        return (int(result), float(result))


NODE_CLASS_MAPPINGS = {
    "Math Operation": MathOperation,
}
