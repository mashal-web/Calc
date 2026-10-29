import math
from statistics import mean, median, variance, pstdev, stdev

def summarize(values):
    if not isinstance(values, list) or not 1 <= len(values) <= 10000:
        raise ValueError("Provide 1–10,000 data values.")
    try: data = [float(x) for x in values]
    except Exception as exc: raise ValueError("All data values must be numeric.") from exc
    if not all(math.isfinite(x) for x in data): raise ValueError("Values must be finite.")
    result = {"count": len(data), "mean": mean(data), "median": median(data),
              "min": min(data), "max": max(data), "population_variance": 0 if len(data)==1 else sum((x-mean(data))**2 for x in data)/len(data),
              "population_stddev": pstdev(data)}
    if len(data) >= 2:
        result["sample_variance"] = variance(data)
        result["sample_stddev"] = stdev(data)
    return result
