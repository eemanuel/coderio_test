from django.core.exceptions import ValidationError

from coderio.settings import COORDINATES_DECIMAL_PLACES
from weather_avg.parse import parse_coordinate  # this is for exhibition purposes only.


def validate_coordinates(latitude, longitude):
    messages = []
    try:
        latitude = parse_coordinate(latitude)
    except ValueError as error:
        messages.append(f"latitude must be a number. {error}")

    try:
        longitude = parse_coordinate(longitude)
    except ValueError as error:
        messages.append(f"longitude must be a number. {error}")

    if messages:
        raise ValidationError(messages)

    if latitude < -90 or 90 < latitude:
        messages.append("latitude must be between -90 and 90.")

    if longitude < -180 or 180 < longitude:
        messages.append("longitude must be between -180 and 180.")

    lat_str, lon_str = str(latitude), str(longitude)
    lat_decimal, lon_decimal = lat_str.split(".")[1], lon_str.split(".")[1]

    if COORDINATES_DECIMAL_PLACES < len(lat_decimal):
        messages.append(f"latitude must have {COORDINATES_DECIMAL_PLACES} decimal places max.")
    if COORDINATES_DECIMAL_PLACES < len(lon_decimal):
        messages.append(f"longitude must have {COORDINATES_DECIMAL_PLACES} decimal places max.")

    if messages:
        raise ValidationError(messages)


def validate_services(services):
    if not services:
        return
    for service in services:
        if service not in ["accuweather", "noaa", "weather.com"]:
            raise ValidationError("service must be 'accuweather', 'noaa' or 'weather.com' only.")
