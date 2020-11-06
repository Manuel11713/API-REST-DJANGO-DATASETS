from django.contrib.gis.db import models

class DataSet(models.Model):
    name = models.CharField(max_length=95)
    date = models.DateField()


class Row(models.Model):
    dataset = models.ForeignKey(DataSet, on_delete=models.CASCADE)
    client_id = models.IntegerField()
    client_name = models.CharField(max_length=45)
    point = models.PointField()