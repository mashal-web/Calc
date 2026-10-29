import sympy as sp
from .validation import bounded_text

def solve_equation(equation, variable="x"):
    equation = bounded_text(equation, "Equation", 300).strip()
    if not equation or variable not in ("x", "y", "z"):
        raise ValueError("Enter an equation and choose x, y, or z.")
    if equation.count("=") > 1:
        raise ValueError("Use only one equals sign.")
    try:
        if "=" in equation:
            left, right = equation.split("=")
            lhs = sp.sympify(left, locals={variable: sp.Symbol(variable)})
            rhs = sp.sympify(right, locals={variable: sp.Symbol(variable)})
            expr = lhs - rhs
        else:
            expr = sp.sympify(equation, locals={variable: sp.Symbol(variable)})
        sym = sp.Symbol(variable)
        solutions = sp.solve(expr, sym)
        if not solutions:
            if sp.simplify(expr) == 0:
                return ["All values satisfy the equation."]
            raise ValueError("No solution found.")
        return [str(sp.simplify(s)) for s in solutions]
    except ValueError:
        raise
    except Exception as exc:
        raise ValueError("Invalid equation. Use standard arithmetic and one variable.") from exc
