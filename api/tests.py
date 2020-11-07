from django.test import TestCase, Client
from datetime import date
import os
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
    test_root = os.path.abspath(os.path.dirname(__file__))

    def setUp(self):
        self.c = Client()
    
    def test_postDataSets(self):
  
        #-----Test for post DataSets
        route = '/api/v1/datasets'
        with open(os.path.join(self.test_root, './assets/backend.csv')) as fileU:
            response = self.c.post(route, {'name': 'dataset1', 'file': fileU})
        self.assertEqual(response.status_code,200)
        dataset_id = response.data
    
        #-----Tests for get all Rows
        route = '/api/v1/datasets?number_page=1'
        response = self.c.get(route)
        self.assertEquals(response.status_code,200)
        self.assertIs(type(response.data),list)


        route = '/api/v1/datasets?number_page=2'
        response = self.c.get(route)
        self.assertEquals(response.status_code,200)
        self.assertIs(type(response.data),list)


        #In this case we have just 2 pages
        route = '/api/v1/datasets?number_page=41'
        response = self.c.get(route)
        self.assertEquals(response.status_code,400)
        self.assertIsNot(type(response.data),list)

        
        #-----Tests for get all Rows, filtering by dataset_id, name, point
        route = '/api/v1/rows?dataset_id={}&name=ram&point=19.3475164,-99.2009924'.format(dataset_id)
        response = self.c.get(route)

        self.assertEquals(response.status_code,200)
        self.assertIs(type(response.data),list)
        self.assertEqual(len(response.data),1)

        route = '/api/v1/rows?dataset_id={}&name=horse&point=19.3475164,-99.2009924'.format(dataset_id)#There is't name==horse
        response = self.c.get(route)
        self.assertEquals(response.status_code,200)
        self.assertIs(type(response.data),list)
        self.assertEqual(len(response.data),0)