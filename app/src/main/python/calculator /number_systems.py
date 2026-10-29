def convert_base(value, from_base, to_base):
    if from_base not in (2,8,10,16) or to_base not in (2,8,10,16):
        raise ValueError("Bases supported: 2, 8, 10, 16.")
    try: n = int(str(value).strip(), int(from_base))
    except Exception as exc: raise ValueError("Number is invalid for the selected source base.") from exc
    if n < 0: return "-" + _digits(-n, int(to_base))
    return _digits(n, int(to_base))
def _digits(n, base):
    chars = "0123456789ABCDEF"
    if n == 0: return "0"
    out = ""
    while n:
        n, r = divmod(n, base); out = chars[r] + out
    return out
