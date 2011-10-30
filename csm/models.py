from django.db import models
from django.contrib.auth.models import User

class OwnerType(models.Model):
    name = models.CharField(max_length=50)

class Owner(User):
    #officialcontact = models.ForeignKey('Individual', blank=True, null=True, related_name='+', on_delete=models.SET_NULL)
    #paperless = models.BooleanField()
    #ownertype = models.ForeignKey(OwnerType)
    pass

class Individual(models.Model):
    owner = models.ForeignKey(Owner)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(max_length=75, blank=True)
