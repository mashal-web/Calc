from fractions import Fraction
from decimal import Decimal, InvalidOperation

def simplify_fraction(numerator, denominator):
    if denominator == 0:
        raise ZeroDivisionError("Denominator cannot be zero.")
    f = Fraction(int(numerator), int(denominator))
    return {"numerator": f.numerator, "denominator": f.denominator, "text": str(f)}

def decimal_to_fraction(value, max_denominator=1000000):
    try:
        f = Fraction(Decimal(str(value))).limit_denominator(max_denominator)
    except (InvalidOperation, ValueError, ZeroDivisionError) as exc:
        raise ValueError("Enter a valid finite decimal.") from exc
    return {"numerator": f.numerator, "denominator": f.denominator, "text": str(f)}
