FROM python:3.7-slim-buster

ENV PYTHONUNBUFFERED=1

RUN mkdir /code 

WORKDIR /code

COPY . /code/

RUN apt-get update
RUN apt-get -y install software-properties-common

#Requirements for GDAL
RUN add-apt-repository ppa:ubuntugis/ppa
RUN apt-get install -y apt-transport-https
RUN apt-get -y install gdal-bin libgdal-dev  python-gdal python3-gdal python3-dev
ARG CPLUS_INCLUDE_PATH=/usr/include/gdal
ARG C_INCLUDE_PATH=/usr/include/gdal

COPY . /code/

RUN pip3 install -r requirements.txt

