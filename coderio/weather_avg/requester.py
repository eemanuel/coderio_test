from urllib3.util.retry import Retry

from requests import get, post, Session
from requests.adapters import HTTPAdapter

from coderio.settings import WEATHER_SERVICE_URL


class WeatherRequester:
    URL_BASE = WEATHER_SERVICE_URL
    TIMEOUT = 3  # seconds
    MAX_RETRIES = 3  # retry MAX_RETRIES times in case of requests.exceptions.ConnectionError
    _instance = None

    @classmethod
    def __new__(cls, *args, **kwargs):  # This converts the class in a singleton.
        if isinstance(cls._instance, cls):
            return cls._instance
        cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        session = Session()
        retry = Retry(connect=self.MAX_RETRIES, backoff_factor=0.7)
        http_adapter = HTTPAdapter(max_retries=retry)
        session.mount("http://", http_adapter)
        session.mount("https://", http_adapter)
        self.session = session

    def send_request(self, method, url_path, data):
        if method == "POST":
            response = post(self.URL_BASE + url_path, json=data, timeout=self.TIMEOUT)
        elif method == "GET":
            response = get(self.URL_BASE + url_path, timeout=self.TIMEOUT)
        else:
            raise ValueError("Bad 'method' arg at 'send_request' invocation.")
        response.raise_for_status()  # raise HTTPError if response.status_code != 200
        return response
