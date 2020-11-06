install sudo apt-get install gdal-bin

https://hub.docker.com/r/mdillon/postgis/

'ENGINE': 'django.contrib.gis.db.backends.postgis', 

SERIALIZATION_MODULES = {
    "geojson": "django.contrib.gis.serializers.geojson", 
 }