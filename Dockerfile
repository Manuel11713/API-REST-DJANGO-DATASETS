FROM python:3.6
ENV PYTHONUNBUFFERED=1

RUN mkdir /code 

WORKDIR /code

COPY . /code/

RUN apt-get -y update
RUN apt-get -y upgrade 

RUN apt-get -y install gdal-bin 
RUN apt-get -y install gdal-dev

RUN pip3 install -r requirements.t

COPY . /code/