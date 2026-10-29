import sympy as sp

def _matrix(data):
    if not isinstance(data, list) or not data or len(data) > 8:
        raise ValueError("Matrix must have 1–8 rows.")
    if any(not isinstance(row, list) or not row or len(row) > 8 for row in data):
        raise ValueError("Matrix must have 1–8 columns per row.")
    if len({len(row) for row in data}) != 1:
        raise ValueError("All matrix rows must have equal length.")
    try:
        return sp.Matrix(data)
    except Exception as exc:
        raise ValueError("Matrix entries must be numeric.") from exc

def matrix_operation(operation, a, b=None):
    A = _matrix(a)
    B = _matrix(b) if b is not None else None
    ops = {
        "transpose": lambda: A.T,
        "determinant": lambda: A.det() if A.rows == A.cols else (_ for _ in ()).throw(ValueError("Determinant requires a square matrix.")),
        "inverse": lambda: A.inv() if A.rows == A.cols else (_ for _ in ()).throw(ValueError("Inverse requires a square matrix.")),
        "rank": lambda: sp.Matrix([[A.rank()]]),
        "add": lambda: A + B,
        "subtract": lambda: A - B,
        "multiply": lambda: A * B,
    }
    if operation not in ops:
        raise ValueError("Unsupported matrix operation.")
    try:
        result = ops[operation]()
    except (sp.matrices.exceptions.NonInvertibleMatrixError, ValueError):
        raise
    except Exception as exc:
        raise ValueError("Matrix dimensions are incompatible for this operation.") from exc
    if isinstance(result, sp.MatrixBase):
        return [[str(result[i, j]) for j in range(result.cols)] for i in range(result.rows)]
    return str(result)
