# Coderio Test


#### Problem:

Build a Django application that will connect with 3 external
weather services and provide an average temperature for a given zip lat/lon.

The Django application should have a single url route that takes
in a latitude, longitude, and a list of external services to filter on.

The acceptable filters will be ‘noaa’, ‘weather.com’, and ‘accuweather’.

For example: if the user sends in ‘noaa’ and ‘accuweather’ in the filter list,
then only those two services will be used to calculate the average temperature
for the given lat/lon.

In order to connect with the 3 external APIs, we have created
a simple Flask application that you will run and connect to.

This will prevent you from having to actually integrate
with three external providers.

Please access this application and view the readme here:
https://github.com/otterlogic/mock-weather-api

Although this is a simple application,
please use architecture and design patterns
as you would for a larger and more complex project.
#


#### Guidelines:

* Use Django

* Create a url route that accepts: latitude, longitude, and filters

* Filter the external providers depending on the user input filters

* The response to the request will be a json response
with the average current temperature


#### Bonus (not required):

* Validate the lat/lon with the Google Maps API (not neccesary)

* TEST much Test




## To run in Docker containers

Clone repository:
 
```sh
$  git clone https://github.com/eemanuel/coderio_test.git
```

Create the docker network:

```sh
$  sudo docker network create --driver bridge django-flask-net
```

In one terminal:

```sh
$  cd coderio_test/coderio/
$  sudo docker-compose up
```

In another terminal:

```sh
$  cd coderio_test/flask/
$  sudo docker-compose up
```

## Check in browser the url:

```
http://0.0.0.0:8000/<lat>/<lon>/?services=accuweather&services=noaa&services=weather.com
```

## Add new Service

If you need to include a new service, you must inherit from: 
```
coderio.weather_avg.services.WeatherService
```
and override any methods.
Then add the name as a new WEATHER_SERVICES_MAPPER key
with their correspondent class in the value.
