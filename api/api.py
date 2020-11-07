from rest_framework.views import   APIView
from rest_framework.response import Response
from django.core.paginator import Paginator
from rest_framework import status
from django.contrib.gis.geos import Point
from datetime import date
import pandas as pd
import re

#Models
from .models import DataSet,Row

#Serializers
from .serializers import serializeGIS

class APIDataset(APIView):
    def get(self,request):

        try:
            number_page =  int(request.query_params['number_page'])
        except:
            return Response(data = "number_page should be an integer", status = status.HTTP_400_BAD_REQUEST)
        
        OBJECTS_PER_PAGE = 2

        #We make a pagination
        rows = Row.objects.all().order_by('id')#SELECT * FROM Row;
        pages = Paginator(rows, OBJECTS_PER_PAGE)

        #Number page should be between right bounds.
        if(number_page<=0 or number_page>pages.num_pages):
            return Response(data="number_page should be between 1 and {}".format(pages.num_pages), status=status.HTTP_400_BAD_REQUEST)

        #Divide by number_page
        rows = pages.page(number_page).object_list
        
        #Serialize points to JSON
        rows = serializeGIS(rows)

        return Response(data=rows, status=200)

    def post(self, request):

        #Must be a valid name
        nameFile = request.data["name"]
        if(not nameFile ):
            return Response(data="Please insert a name",status=status.HTTP_400_BAD_REQUEST)
        
        #Must be a file
        uploaded_file = request.data['file']
        if(not uploaded_file ):
            return Response(data="Please select a csv file",status=status.HTTP_400_BAD_REQUEST)

        #First we check if file's extension is a csv
        extension = re.split('\.',uploaded_file._get_name())[-1]
        if( extension != 'csv'):
            return Response(data="Should be a csv file",status=status.HTTP_400_BAD_REQUEST)

        data = pd.read_csv(uploaded_file)
        columns = data.columns
    
        #Must be a valid structure
        if( len(columns) != 4 or 
            (columns[0] != "latitude" or columns[1] != "longitude" or columns[2] != "client_id" or columns[3] != "client_name" )
        ):
            return Response(data = "Wrong format", status = status.HTTP_400_BAD_REQUEST)

        #Check if dataSet exists already.
        try:
            newDataSet = DataSet.objects.get(name=nameFile)
        except:
            newDataSet = DataSet(name = nameFile, date = date.today())
            newDataSet.save()

        #Save row by row.
        for row in data.iterrows():
            row = row[1]
            newPoint = Point(row[0],row[1])
            newRow = Row(point = newPoint, client_id = row[2], client_name = row[3], dataset_id = newDataSet.id)
            newRow.save()
            
        return Response(data=newDataSet.id, status=200)
    

class APIRows(APIView):
    def get(self,request):
        
        #We should get the query params.
        try:
            dataset_id = request.query_params['dataset_id']
            name = request.query_params['name']
            point = request.query_params['point']
            point = re.split(',',point)
        except:
            return Response(data="dataset_id, name and point should be provided in query params") 

        if(len(point) != 2):
            return Response(data="point should have just 2 values",status=status.HTTP_400_BAD_REQUEST)
        
        #Dataset should exists
        try:
            dataset = DataSet.objects.get(id=dataset_id)
        except:
            return Response(data="wrong dataset id",status=status.HTTP_400_BAD_REQUEST)
        
        #Filtering by params
        point = Point(float(point[0]),float(point[1]))
        rows = Row.objects.filter(dataset_id=dataset.id,client_name=name,point=point)
        
        #Serialize points to JSON
        rows = serializeGIS(rows)
        
        return Response(data=rows,status=status.HTTP_200_OK)
 