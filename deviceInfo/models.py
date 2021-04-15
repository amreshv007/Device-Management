from django.db import models
from django.contrib.auth.models import User

class GivenTo(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    barcode = models.IntegerField(default='')
    modelName = models.CharField(max_length=200, default='')
    givento = models.CharField(max_length=200, default='')
    date = models.DateTimeField(max_length=255, default='')

    def __str__(self):
        return str(self.barcode)


class TakenFrom(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    barcode = models.IntegerField(default='')
    modelName = models.CharField(max_length=200, default='')
    takenfrom = models.CharField(max_length=200, default='')
    date = models.DateTimeField(max_length=255, default='')

    def __str__(self):
        return str(self.barcode)