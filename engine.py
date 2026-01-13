import ast
import operator

OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}

def avaliar(expr: str) -> str:
    def _eval(node):
        if isinstance(node, ast.Constant):
            return node.value

        if isinstance(node, ast.BinOp):
            return OPS[type(node.op)](
                _eval(node.left),
                _eval(node.right)
            )

        raise ValueError("Expressão inválida")

    try:
        expr = expr.replace("x", "*")
        tree = ast.parse(expr, mode="eval")
        resultado = _eval(tree.body)

        if isinstance(resultado, float) and resultado.is_integer():
            resultado = int(resultado)

        return str(resultado), False

    except ZeroDivisionError:
        return "Erro: divisão por zero", True

    except:
        return "Erro", True

