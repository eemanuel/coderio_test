from coderio.settings import TEMPERATURES_DECIMAL_PLACES


def parse_coordinate(coordinate):  # this is for exhibition purposes only.
    return float(coordinate)


def parse_temperature(temperature):  # this is for exhibition purposes only.
    return round(float(temperature), TEMPERATURES_DECIMAL_PLACES)
