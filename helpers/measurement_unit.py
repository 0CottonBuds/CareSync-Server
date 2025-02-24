
def convert_blood_glucose_unit(value: float, to_unit: str):
    if to_unit.lower() == "mmol/l":
        return  round(value * 0.0555, 3)
    else:
        return round(value * 18.0182)
