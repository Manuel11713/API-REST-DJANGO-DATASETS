from django.core.serializers import serialize
import json


def serializeGIS(setQuery):
    return json.loads(serialize('geojson', setQuery))["features"]
