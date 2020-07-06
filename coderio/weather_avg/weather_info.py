from abc import ABC, abstractmethod

from coderio.settings import TEMPERATURES_DECIMAL_PLACES
from utils.utils import farenheit_to_celsius, get_value


class WeatherInfo(ABC):
    DECIMAL_PLACES = TEMPERATURES_DECIMAL_PLACES

    def __init__(self, payload):
        celsius, fahrenheit = self.parse(payload)
        self.celsius = round(float(celsius), self.DECIMAL_PLACES)
        self.fahrenheit = round(float(fahrenheit), self.DECIMAL_PLACES)

    @abstractmethod
    def parse(self, payload):
        pass


class AccuweatherInfo(WeatherInfo):
    def parse(self, payload):
        forecastday = get_value(payload, ["simpleforecast", "forecastday"])
        current = forecastday[0]["current"]
        return current["celsius"], current["fahrenheit"]


class NoaaInfo(WeatherInfo):
    def parse(self, payload):
        current = get_value(payload, ["today", "current"])
        return current["celsius"], current["fahrenheit"]


class WeatherDotComInfo(WeatherInfo):
    def parse(self, payload):
        key_path_list = ["query", "results", "channel", "condition", "temp"]
        fahrenheit = get_value(payload, key_path_list)
        celsius = farenheit_to_celsius(fahrenheit)
        return celsius, fahrenheit
