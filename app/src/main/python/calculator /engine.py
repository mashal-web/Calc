import math
import sympy as sp
from .parser import parse_expression

def _format(value, precision):
    if isinstance(precision, bool) or not isinstance(precision, int) or not 2 <= precision <= 15:
        raise ValueError("Precision must be an integer from 2 to 15.")
    if value.has(sp.zoo, sp.nan, sp.oo, -sp.oo):
        raise ValueError("Result is undefined or infinite.")
    exact = str(value)
    if value.is_number:
        try:
            approx = sp.N(value, precision)
            if approx.is_real:
                n = float(approx)
                if not math.isfinite(n):
                    raise ValueError("Result is outside the supported numeric range.")
                decimal = f"{n:.{precision}g}"
            else:
                decimal = str(approx)
        except (TypeError, ValueError, OverflowError):
            decimal = str(sp.N(value, precision))
    else:
        decimal = str(value)
    return {"exact": exact, "approx": decimal, "is_exact": bool(value.is_Rational or value.is_Integer or not value.is_number)}

def calculate(expression, angle_mode="DEG", precision=10):
    expr = parse_expression(expression, angle_mode=angle_mode)
    result = sp.simplify(expr)
    if result.is_number and result.is_finite is False:
        raise ValueError("Result is undefined or infinite.")
    return {"expression": expression, "result": _format(result, precision)}
