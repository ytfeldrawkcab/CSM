from django.db import models
from django.contrib.auth.models import User

class OwnerType(models.Model):
    name = models.CharField(max_length=50)
    def __unicode__(self):
        return self.name

class Owner(User):
    officialcontact = models.ForeignKey('Individual', blank=True, null=True, related_name='+', on_delete=models.SET_NULL)
    paperless = models.BooleanField()
    ownertype = models.ForeignKey(OwnerType)
    address1 = models.CharField(max_length=200)
    address2 = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=2)
    zipcode = models.CharField(max_length=10)
    def __unicode__(self):
        return self.username
    def save(self):
        if self.officialcontact:
            self.email = self.officialcontact.email
        else:
            self.email = ''
        super(Owner, self).save()

class Individual(models.Model):
    owner = models.ForeignKey('Owner')
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(max_length=75, blank=True)
    def __unicode__(self):
        return self.firstname + ' ' + self.lastname

#class Election(models.Model):
#    name = models.CharField(max_length=100)
#    description = models.TextField()
#    beginvoting = models.DateField()
#    endvoting = models.DateField()
#    maxchoices = models.IntegerField()

#class Candidate(models.Model):
#    election = models.ForeignKey(Election)
#    name = models.CharField(max_length=50)
#    description = models.TextField()

#class OwnerVote(models.Model):
#    owner = models.ForeignKey(Owner)
#    candidate = models.ForeignKey(Candidate)
#    datesubmitted = models.DateField(auto_now=True)
