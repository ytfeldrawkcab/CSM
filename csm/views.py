from csm.models import *
from csm.forms import *

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

#public functions           
def findparentinstance(parentforms, lookupprefix):
    for parentform in parentforms:
        if parentform.prefix == lookupprefix:
            return parentform.instance
    return None
            
def findparentprefix(parentforms, lookupinstance):
    for parentform in parentforms:
        if parentform.instance == lookupinstance:
            return parentform.prefix

#owner management
def editowner(request, ownerid=None):
    if request.method == 'GET':
        if ownerid:
            owner = Owner.objects.get(username=ownerid)
        else:
            owner = None
        
        individuals = Individual.objects.filter(owner=owner)
        i = 0
        individualforms = []
        for individual in individuals:
            i += 1
            individualform = IndividualForm(instance=individual, prefix='i'+str(i))
            individualforms.append(individualform)
        
        ownerform = OwnerForm(instance=owner, initial={'individualcount':i})
        
        return render_to_response('owners/edit.html', RequestContext(request, {'form':ownerform, 'individualforms':individualforms}))
    else:
        passedvalidation = True
        individualcount = request.POST['individualcount']
        individualforms = []
        
        ownerform = OwnerForm(request.POST)
        if not ownerform.is_valid():
            passedvalidation = False
            
        for i in xrange(1, int(individualcount)+1):
            individualform = IndividualForm(request.POST, prefix='i'+str(i))
            individualforms.append(individualform)
            if not individualform.is_valid():
                passedvalidation = False
            
        if passedvalidation == False:
            return render_to_response('owners/edit.html', RequestContext(request, {'form':ownerform, 'individualforms':individualforms}))
        
        else:
            owner = ownerform.save()
            
            for individualform in individualforms:
                individual = individualform.save(commit=False)
                individual.owner = owner
                if individualform.cleaned_data['delete'] == 0:
                    individual.save()
                elif individual.pk:
                    individual.delete()
            
            #set official contact here and then save     
            #owner.save()
            
            return HttpResponseRedirect('/owners/' + str(owner.username) + '/edit/')
            
def addindividual(request):
    prefix = request.GET['prefix']
    individualform = IndividualForm(prefix='i'+str(prefix))
    
    return render_to_response('owners/individual.html', {'individualform':individualform})
