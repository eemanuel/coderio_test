from django.urls import path
from weather_avg.views import weather_average_view


urlpatterns = [path("<path:latitude>/<path:longitude>/", weather_average_view, name="weather_avg")]
