import ast
import operator


OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos
}


def calculate(expression):

    try:
        tree = ast.parse(expression, mode="eval")

        return evaluate_node(tree.body)

    except ZeroDivisionError:
        return "Calculation error: Division by zero."

    except Exception as e:
        return f"Calculation error: {e}"


def evaluate_node(node):

    if isinstance(node, ast.Constant):

        if isinstance(node.value, (int, float)):
            return node.value

        raise ValueError("Only numbers are allowed.")

    if isinstance(node, ast.UnaryOp):

        operator_function = OPERATORS.get(type(node.op))

        if operator_function is None:
            raise ValueError("Unsupported operator.")

        return operator_function(
            evaluate_node(node.operand)
        )

    if isinstance(node, ast.BinOp):

        operator_function = OPERATORS.get(type(node.op))

        if operator_function is None:
            raise ValueError("Unsupported operator.")

        left = evaluate_node(node.left)
        right = evaluate_node(node.right)

        return operator_function(left, right)

    raise ValueError(
        "Only mathematical expressions are allowed."
    )


def calculate_profit_margin(profit, sales):

    if sales == 0:
        return 0

    return (profit / sales) * 100