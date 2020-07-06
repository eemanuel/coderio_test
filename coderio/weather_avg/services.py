from abc import ABC, abstractmethod

from utils.utils import farenheit_to_celsius, get_value
from weather_avg.parse import parse_temperature  # this is for exhibition purposes only.
from weather_avg.requester import WeatherRequester


class WeatherService(ABC):
    requester = WeatherRequester()
    method = None
    _instance = None

    @classmethod
    def __new__(cls, *args, **kwargs):  # This converts the class in a singleton.
        if isinstance(cls._instance, cls):
            return cls._instance
        cls._instance = super().__new__(cls)
        return cls._instance

    @abstractmethod
    def get_url_path(self, latitude, longitude):
        """
        It return the url path.
        For example:
        return f"/url_chunk?lat={latitude}&lon={longitude}"
        """

        pass

    @abstractmethod
    def parse(self, payload):
        """
        It parse the requester response (payload).
        For example:
        current = payload["current_temperature"]
        return current["celsius"], current["fahrenheit"]
        """

        pass

    def get_data(self, latitude, longitude):
        """
        Only override this method if any data is neccesary to the request.
        For example:
        return (latitude, longitude)  # this is the request.data
        """

        return None

    def get_current_temperature(self, latitude, longitude):
        """
        Send request to service url, parse the response and return the current temperature.
        """

        data = self.get_data(latitude, longitude)
        url_path = self.get_url_path(latitude, longitude)
        response = self.requester.send_request(self.method, url_path, data)
        celsius, fahrenheit = self.parse(response.json())
        celsius, fahrenheit = parse_temperature(celsius), parse_temperature(fahrenheit)
        return {"fahrenheit": fahrenheit, "celsius": celsius}


class AccuweatherService(WeatherService):
    method = "GET"

    def get_url_path(self, latitude, longitude):
        return f"/accuweather?latitude={latitude}&longitude={longitude}"

    def parse(self, payload):
        forecastday = get_value(payload, ["simpleforecast", "forecastday"])
        current = forecastday[0]["current"]
        return current["celsius"], current["fahrenheit"]


class NoaaService(WeatherService):
    method = "GET"

    def get_url_path(self, latitude, longitude):
        return f"/noaa?latlon={latitude},{longitude}"

    def parse(self, payload):
        current = get_value(payload, ["today", "current"])
        return current["celsius"], current["fahrenheit"]


class WeatherDotComService(WeatherService):
    method = "POST"

    def get_url_path(self, latitude, longitude):
        return "/weatherdotcom"

    def get_data(self, latitude, longitude):
        return {"lat": latitude, "lon": longitude}

    def parse(self, payload):
        key_path_list = ["query", "results", "channel", "condition", "temp"]
        fahrenheit = get_value(payload, key_path_list)
        celsius = farenheit_to_celsius(fahrenheit)
        return celsius, fahrenheit


WEATHER_SERVICES_MAPPER = {"accuweather": AccuweatherService, "noaa": NoaaService, "weather.com": WeatherDotComService}
