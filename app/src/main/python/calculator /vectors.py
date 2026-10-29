import math

def vector_operation(operation, a, b=None):
    if not isinstance(a, list) or not 1 <= len(a) <= 3:
        raise ValueError("Vector must contain 1–3 numeric components.")
    try: A = [float(x) for x in a]
    except Exception as exc: raise ValueError("Vector components must be numeric.") from exc
    B = None
    if b is not None:
        if not isinstance(b, list): raise ValueError("Second vector must be a list.")
        try: B = [float(x) for x in b]
        except Exception as exc: raise ValueError("Vector components must be numeric.") from exc
    if operation == "magnitude": return math.sqrt(sum(x*x for x in A))
    if operation == "unit":
        m = math.sqrt(sum(x*x for x in A))
        if m == 0: raise ValueError("Zero vector has no unit vector.")
        return [x/m for x in A]
    if B is None or len(A) != len(B): raise ValueError("Two vectors of equal dimension are required.")
    if operation == "add": return [x+y for x,y in zip(A,B)]
    if operation == "subtract": return [x-y for x,y in zip(A,B)]
    if operation == "dot": return sum(x*y for x,y in zip(A,B))
    if operation == "cross" and len(A) == len(B) == 3:
        return [A[1]*B[2]-A[2]*B[1], A[2]*B[0]-A[0]*B[2], A[0]*B[1]-A[1]*B[0]]
    if operation == "angle":
        denom = math.sqrt(sum(x*x for x in A)*sum(x*x for x in B))
        if denom == 0: raise ValueError("Angle is undefined for a zero vector.")
        return math.degrees(math.acos(max(-1, min(1, sum(x*y for x,y in zip(A,B))/denom))))
    raise ValueError("Unsupported vector operation.")
