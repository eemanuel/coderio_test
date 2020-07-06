from requests.exceptions import HTTPError, RequestException

from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views.decorators.http import require_GET

from weather_avg.calculate import WeatherCalculator
from weather_avg.validators import validate_coordinates, validate_services


@require_GET
def weather_average_view(request, latitude, longitude):
    """
    Calculate the average temperature in fahrenheit and celsius
    beetween the many external services information.
    """

    services = request.GET.getlist("services")
    try:
        validate_coordinates(latitude, longitude)
        validate_services(services)
    except ValidationError as error:
        return JsonResponse({"error": error.messages}, status=400)

    calculate = WeatherCalculator(latitude, longitude, services)
    try:
        weather_avg = calculate.weather_avg()
    except (HTTPError, RequestException) as error:
        return JsonResponse({"error": str(error)}, status=409)  # this errors should be raised in the requester.
    return JsonResponse(weather_avg)
