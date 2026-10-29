"""Safe expression parser using SymPy's restricted transformations and an explicit function allowlist."""
import re
import sympy as sp
from sympy.parsing.sympy_parser import (
    parse_expr, standard_transformations, implicit_multiplication_application,
    convert_xor, rationalize
)
from .validation import bounded_text

TRANSFORMS = standard_transformations + (
    implicit_multiplication_application, convert_xor, rationalize
)
FUNCTIONS = {
    "sin": sp.sin, "cos": sp.cos, "tan": sp.tan,
    "asin": sp.asin, "acos": sp.acos, "atan": sp.atan,
    "sinh": sp.sinh, "cosh": sp.cosh, "tanh": sp.tanh,
    "asinh": sp.asinh, "acosh": sp.acosh, "atanh": sp.atanh,
    "sqrt": sp.sqrt, "abs": sp.Abs, "ln": sp.log, "log": sp.log,
    "log10": lambda x: sp.log(x, 10), "exp": sp.exp,
    "floor": sp.floor, "ceil": sp.ceiling, "factorial": sp.factorial,
    "gcd": sp.gcd, "lcm": sp.ilcm, "re": sp.re, "im": sp.im,
    "conj": sp.conjugate, "arg": sp.arg,
}
CONSTANTS = {"pi": sp.pi, "e": sp.E, "I": sp.I, "oo": sp.oo}
_ALLOWED_CHARS = re.compile(r"^[0-9A-Za-z_+\-*/().,%\s^!]+$")

def parse_expression(source, *, angle_mode="DEG"):
    source = bounded_text(source, "Expression", 300).strip()
    if not source:
        raise ValueError("Enter an expression.")
    if not _ALLOWED_CHARS.fullmatch(source):
        raise ValueError("Expression contains unsupported characters.")
    if source.count("(") + source.count(")") > 60:
        raise ValueError("Expression nesting is too large.")
    # Convert common calculator syntax before parsing.
    source = source.replace("π", "pi").replace("×", "*").replace("÷", "/")
    source = source.replace("−", "-").replace("√", "sqrt")
    source = source.replace("%", "/100")
    if "!" in source:
        source = re.sub(r"(\b\d+(?:\.\d+)?|\))!", r"factorial(\1)", source)
    local = dict(FUNCTIONS)
    local.update(CONSTANTS)
    # Degree mode is implemented by wrapping direct trig inputs in radians.
    if angle_mode not in ("DEG", "RAD"):
        raise ValueError("Angle mode must be DEG or RAD.")
    if angle_mode == "DEG":
        for fn in ("sin", "cos", "tan"):
            local[fn] = (lambda f: lambda x: f(x * sp.pi / 180))(FUNCTIONS[fn])
        for fn in ("asin", "acos", "atan"):
            local[fn] = (lambda f: lambda x: f(x) * 180 / sp.pi)(FUNCTIONS[fn])
    # Prevent names not in the allowlist. parse_expr uses eval internally; locals/globals
    # are tightly restricted, and the character/name allowlist blocks Python syntax.
    names = set(re.findall(r"[A-Za-z_][A-Za-z_0-9]*", source))
    allowed = set(local) | {"x", "y", "z"}
    unknown = names - allowed
    if unknown:
        raise ValueError("Unsupported name/function: " + ", ".join(sorted(unknown)))
    try:
        return parse_expr(source, local_dict=local, global_dict={
            "__builtins__": {}, "Integer": sp.Integer, "Float": sp.Float,
            "Rational": sp.Rational, "Symbol": sp.Symbol, "Add": sp.Add,
            "Mul": sp.Mul, "Pow": sp.Pow, "factorial": sp.factorial
        }, transformations=TRANSFORMS, evaluate=True)
    except Exception as exc:
        raise ValueError("Invalid expression. Check operators, parentheses, and function arguments.") from exc
