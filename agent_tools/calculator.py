def calculator(input: str) -> str:
    try:
        return str(eval(input))
    except Exception as e:
        return f"Error: {str(e)}"
