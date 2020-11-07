from django.test import TestCase, Client
from datetime import date

from django.contrib.gis.geos import Point
from .models import DataSet,Row

from .serializers import serializeGIS

#Tests for Models
class ModelsTests(TestCase):
    test_name_DS = "dataset1"

    def setUp(self):
            DataSet.objects.create(name = self.test_name_DS, date = date.today()) 

            Row.objects.create(point = Point(6,1), client_id = 1, client_name = "foo", dataset_id = 1)
            Row.objects.create(point = Point(91,128), client_id = 2, client_name = "bar", dataset_id = 1)
            Row.objects.create(point = Point(25,51), client_id = 3, client_name = "cris", dataset_id = 1)

            
    
    def test_DataSet(self):
        dataset1 = DataSet.objects.get(name = self.test_name_DS)
        
        #Trying to get an unexisting dataset
        try:
            dataset2 = DataSet.objects.get(name ="foo_bar")
        except:
            dataset2 = None
    
        #Assets for Datasets
        self.assertEqual(dataset1.name, self.test_name_DS)
        self.assertEqual(dataset1.date, dataset1.date.today())
        self.assertEqual(dataset2, None)

        #Asserts for Rows
        rows = Row.objects.filter(dataset_id=1)
        rows = serializeGIS(rows)

        #Serlize Gis works
        self.assertIs(type(rows), list)
        self.assertIs(len(rows), 3)

class RoutesTests(TestCase):
    setUp(self):
        

