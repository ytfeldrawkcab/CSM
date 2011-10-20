from django.db import models
from django.contrib.auth.models import User

class Owner(User):
    pass

class Individual(models.Model):
    owner = models.ForeignKey(Owner)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=75)
