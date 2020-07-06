from statistics import mean

from weather_avg.requester import WeatherRequester
from weather_avg.services import WEATHER_SERVICES_MAPPER


class WeatherCalculator:
    def __init__(self, latitude, longitude, services):
        self.latitude = latitude
        self.longitude = longitude
        if not services:
            self.services = WEATHER_SERVICES_MAPPER.keys()
        else:
            self.services = services

    def weather_avg(self):
        weather_infos = []
        for service in self.services:
            service = WEATHER_SERVICES_MAPPER.get(service)
            service_instance = service()
            current_temperature = service_instance.get_current_temperature(self.latitude, self.longitude)
            weather_infos.append(current_temperature)
        celsius = [info["celsius"] for info in weather_infos]
        fahrenheits = [info["fahrenheit"] for info in weather_infos]
        return {"fahrenheit": round(mean(fahrenheits), 1), "celsius": round(mean(celsius), 1)}
