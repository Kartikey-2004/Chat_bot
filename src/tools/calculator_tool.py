from langchain.tools import tool
import math


@tool
def calculator(expression: str) -> str:
    """
    Evaluate mathematical expressions.
    Input should be a valid math expression.
    """

    allowed = {
        "log10": math.log10,
        "sqrt": math.sqrt,
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
    }

    try:
        result = eval(
            expression,
            {"__builtins__": {}},
            allowed,
        )
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"
