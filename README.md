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
$  cd coderio/
$  sudo docker-compose up
```

In another terminal:

```sh
$  cd flask/
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
and override the correspondient methods.
Then add the name as a new WEATHER_SERVICES_MAPPER key
with their correspondient class in the value.
