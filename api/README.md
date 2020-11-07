sudo apt-get install gdal-bin

https://hub.docker.com/r/mdillon/postgis/

'ENGINE': 'django.contrib.gis.db.backends.postgis', 

SERIALIZATION_MODULES = {
    "geojson": "django.contrib.gis.serializers.geojson", 
}

sudo docker run --name post-gis -p 5432:5432 -d -e POSTGRES_PASSWORD=abraxa mdillon/postgis 

python3 manage.py migrate


python3 manage.py runserver

sudo docker-compose run web django-admin startproject composeexample .

