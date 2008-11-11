from django.db import models

class printer_admin(models.Model):
    make = models.CharField(max_length=200,blank=True)
    model = models.CharField(max_length=200,blank=True)
    date = models.DateTimeField('date logged',blank=True)
    location = models.CharField(max_length=200,blank=True)
    totalcount = models.IntegerField(blank=True)
    colourcount = models.IntegerField(blank=True)
    monocount = models.IntegerField(blank=True)
    cyancount = models.IntegerField(blank=True)
    magcount = models.IntegerField(blank=True)
    yelcount = models.IntegerField(blank=True)
    blackcount = models.IntegerField(blank=True)
    drumcount = models.IntegerField(blank=True)
    difftotal = models.IntegerField(blank=True)
