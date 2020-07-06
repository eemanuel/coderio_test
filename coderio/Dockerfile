FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /source
WORKDIR /source
COPY requirements/base.txt /source/
RUN pip3 install -r base.txt  # change to local.txt if you go to debbugging
COPY . /source/
