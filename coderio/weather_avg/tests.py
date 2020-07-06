from itertools import combinations
from pytest import mark
from requests.exceptions import ConnectionError, HTTPError
from unittest.mock import patch

from django.test import Client
from django.urls import reverse


def create_queryparams_list(all_services, add_none=False):
    """
    It returns a queryparams combinations list, to emulate 
    url chunks as "?services=accuweather&services=noaa&services=weather.com"
    """

    queryparams = []
    services_combinations = combinations(all_services, 2)
    queryparams = [{"services": service_combination} for service_combination in services_combinations]
    if not add_none:
        queryparams.append(None)
    return [{"services": all_services}] + queryparams


class TestWeatherAverageView:
    client = Client()

    def _get_data(self, keyword_args, query_params=None):
        return self.client.get(reverse("weather_avg", kwargs=keyword_args), query_params)

    @mark.coordinates
    @mark.parametrize(
        "keyword_args",
        [
            {"latitude": 45.012345, "longitude": 100.765432},
            {"latitude": -45.7, "longitude": -100.7},
            {"latitude": 90, "longitude": 180},
        ],
    )
    @mark.parametrize("queryparams", create_queryparams_list(["accuweather", "noaa", "weather.com"]))
    def test_success(self, keyword_args, queryparams):
        """
        Testing if the average is successfully returned whith many diferents queryparams.
        """

        response = self._get_data(keyword_args, queryparams)
        data = response.json()
        assert isinstance(data.get("fahrenheit"), float)
        assert isinstance(data.get("celsius"), float)
        assert response.status_code == 200

    @mark.coordinates
    @mark.parametrize("latitude", [-90.000001, 90.000001])
    def test_bad_latitude(self, latitude):
        """
        Testing if the average is not returned whith only bad latitude value.
        """

        keyword_args = {"latitude": latitude, "longitude": 100.765432}
        response = self._get_data(keyword_args)
        data = response.json()
        error = data.get("error")
        assert error == ["latitude must be between -90 and 90."]
        assert response.status_code == 400

    @mark.coordinates
    @mark.parametrize("longitude", [-180.000001, 180.000001])
    def test_bad_longitude_value(self, longitude):
        """
        Testing if the average is not returned whith only bad longitude value.
        """

        keyword_args = {"latitude": 45.765432, "longitude": longitude}
        response = self._get_data(keyword_args)
        data = response.json()
        error = data.get("error")
        assert error == ["longitude must be between -180 and 180."]
        assert response.status_code == 400

    @mark.coordinates
    @mark.parametrize("latitude", [90.000001, -90.000001])
    @mark.parametrize("longitude", [180.000001, -180.000001])
    def test_bad_latitude_and_longitude_values(self, latitude, longitude):
        """
        Testing if the average is not returned whith bad coordinates values.
        """

        keyword_args = {"latitude": latitude, "longitude": longitude}
        response = self._get_data(keyword_args)
        data = response.json()
        error = data.get("error")
        assert error == ["latitude must be between -90 and 90.", "longitude must be between -180 and 180."]
        assert response.status_code == 400

    @mark.coordinates
    @mark.parametrize(
        "keyword_args, expected_error",
        [
            (
                {"latitude": 90.765432, "longitude": "Buenos Aires longitude"},
                ["longitude must be a number. could not convert string to float: 'Buenos Aires longitude'"],
            ),
            (
                {"latitude": "Buenos Aires latitude", "longitude": 180.765432},
                ["latitude must be a number. could not convert string to float: 'Buenos Aires latitude'"],
            ),
            (
                {"latitude": "Córdoba latitude", "longitude": "Córdoba longitude"},
                [
                    "latitude must be a number. could not convert string to float: 'Córdoba latitude'",
                    "longitude must be a number. could not convert string to float: 'Córdoba longitude'",
                ],
            ),
        ],
    )
    def test_bad_latitude_and_or_longitude_fromat(self, keyword_args, expected_error):
        """
        Testing if the average is not returned whith  bad latitude and/or longitude formats.
        """

        response = self._get_data(keyword_args)
        data = response.json()
        assert data.get("error") == expected_error
        assert response.status_code == 400

    @mark.coordinates
    @mark.parametrize(
        "keyword_args, expected_error",
        [
            ({"latitude": 45.7654321, "longitude": 100.765432}, ["latitude must have 6 decimal places max."]),
            ({"latitude": 45.765432, "longitude": 100.7654321}, ["longitude must have 6 decimal places max."]),
            (
                {"latitude": 45.7654321, "longitude": 100.7654321},
                ["latitude must have 6 decimal places max.", "longitude must have 6 decimal places max."],
            ),
        ],
    )
    def test_bad_latitude_and_or_longitude_length(self, keyword_args, expected_error):
        """
        Testing if the average is not returned whith bad coordinates values.
        """

        response = self._get_data(keyword_args)
        data = response.json()
        assert data.get("error") == expected_error
        assert response.status_code == 400

    @mark.queryparams
    @mark.parametrize("queryparams", create_queryparams_list(["noaa", "radio 10", "telefe"], add_none=True))
    def test_bad_queryparams_values(self, queryparams):
        """
        Testing if the average is not returned whith bad queryparams values.
        """

        keyword_args = {"latitude": 45.012345, "longitude": 100.765432}
        response = self._get_data(keyword_args, queryparams)
        data = response.json()
        error = data.get("error")
        assert error == ["service must be 'accuweather', 'noaa' or 'weather.com' only."]
        assert response.status_code == 400

    @mark.queryparams
    def test_queryparams_bad_format(self):
        """
        Testing if the average is not returned whith bad format in queryparams.
        """

        keyword_args = {"latitude": 45.012345, "longitude": 100.765432}
        queryparams = {"services": 666}
        response = self._get_data(keyword_args, queryparams)
        data = response.json()
        assert data.get("error") == ["service must be 'accuweather', 'noaa' or 'weather.com' only."]
        assert response.status_code == 400

    @mark.requester
    @patch("weather_avg.requester.WeatherRequester.send_request")
    def test_requester_connection_error(self, send_request_mock):
        """
        Testing if the average is not returned
        when the requester get or post raise a ConnectionError.
        """

        send_request_mock.side_effect = ConnectionError()

        keyword_args = {"latitude": 45.012345, "longitude": 100.765432}
        response = self._get_data(keyword_args)
        data = response.json()
        assert data.get("error") is not None
        assert response.status_code == 409

    @mark.requester
    @patch("weather_avg.requester.WeatherRequester.send_request")
    def test_bad_requester_response(self, send_request_mock):
        """
        Testing if the average is not returned
        when raise_for_status method in the requester raise an HTTPError.
        """

        send_request_mock.side_effect = HTTPError()

        keyword_args = {"latitude": 45.012345, "longitude": 100.765432}
        response = self._get_data(keyword_args)
        data = response.json()
        assert data.get("error") is not None
        assert response.status_code == 409
