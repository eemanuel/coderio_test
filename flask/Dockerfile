FROM python:3

RUN apt install git
RUN git clone https://github.com/shipwell/mock-weather-api.git
RUN pip install -r mock-weather-api/requirements.txt

ENV FLASK_APP=app
ENV FLASK_RUN_PORT=8080
WORKDIR /mock-weather-api
