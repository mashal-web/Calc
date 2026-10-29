UNITS = {
 "length": {"m":1, "km":1000, "cm":.01, "mm":.001, "mi":1609.344, "ft":.3048, "in":.0254},
 "area": {"m2":1, "km2":1e6, "cm2":1e-4, "ft2":.09290304, "acre":4046.8564224},
 "volume": {"m3":1, "L":.001, "mL":1e-6, "cm3":1e-6, "ft3":.028316846592, "gal_us":.003785411784},
 "mass": {"kg":1, "g":.001, "mg":1e-6, "lb":.45359237, "tonne":1000},
 "time": {"s":1, "min":60, "h":3600, "day":86400},
 "speed": {"m/s":1, "km/h":1/3.6, "mph":.44704, "ft/s":.3048},
 "acceleration": {"m/s2":1, "ft/s2":.3048},
 "force": {"N":1, "kN":1000, "lbf":4.4482216152605},
 "pressure": {"Pa":1, "kPa":1000, "MPa":1e6, "bar":100000, "psi":6894.757293168},
 "energy": {"J":1, "kJ":1000, "cal":4.184, "kWh":3600000, "ft_lbf":1.3558179483},
 "power": {"W":1, "kW":1000, "hp":745.6998716},
 "angle": {"rad":1, "deg":0.017453292519943295},
 "data": {"B":1, "kB":1000, "MB":1e6, "GB":1e9, "KiB":1024, "MiB":1048576, "GiB":1073741824},
}
def convert_units(value, from_unit, to_unit):
    try: value = float(value)
    except (ValueError, TypeError) as exc: raise ValueError("Value must be numeric.") from exc
    if from_unit in ("C","F","K") and to_unit in ("C","F","K"):
        c = value if from_unit=="C" else (value-32)*5/9 if from_unit=="F" else value-273.15
        out = c if to_unit=="C" else c*9/5+32 if to_unit=="F" else c+273.15
        return out
    for category, units in UNITS.items():
        if from_unit in units and to_unit in units:
            return value * units[from_unit] / units[to_unit]
    raise ValueError("Units are incompatible or unsupported. Temperature units: C, F, K.")
