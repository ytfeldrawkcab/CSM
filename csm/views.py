from csm.models import *
from csm.forms import *

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.core.exceptions import ObjectDoesNotExist

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

def searchcriteria(GET):
    if 'searchfield' in GET:
        querystring = GET['querystring']
        searchfield = GET['searchfield']
    else:
        querystring = ''
        searchfield = ''
    return (querystring, searchfield)

#home selection based on usertype
@login_required
def selecthome(request):
    try:
        request.user.owner
        return editowner(request)
    except ObjectDoesNotExist:
        return HttpResponseRedirect('/owners/')

#owner management
@login_required
def editowner(request, ownerid=None):
    try:
        if request.user.owner and ownerid == None:
            ownerid = request.user.owner.username
        elif request.user.owner and ownerid != request.user.owner.username:
            return HttpResponse("You can't view this owner's details.")
        admin = False
    except ObjectDoesNotExist:
        admin = True
    
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
        
        if admin == True:
            ownerform = OwnerMasterForm(instance=owner, initial={'individualcount':i})
        else:
            ownerform = OwnerEditForm(instance=owner, initial={'individualcount':i})
            ownerform.username = owner.username
            ownerform.ownertype = owner.ownertype
            
        if owner:
            ownerform.officialcontactprefix = findparentprefix(individualforms, owner.officialcontact)
            if owner.ownertype.pk == 2 and i > 0:
                ownerform.maxindividuals = 1
        
        return render_to_response('owners/edit.html', RequestContext(request, {'form':ownerform, 'individualforms':individualforms}))
    else:
        passedvalidation = True
        individualcount = request.POST['individualcount']
        individualforms = []
        
        try:
            request.user.owner
            admin = False
            print 'test'
        except ObjectDoesNotExist:
            admin = True
        
        if admin == True:
            ownerform = OwnerMasterForm(request.POST)
        else:
            owner = Owner.objects.get(pk=request.POST['pk'])
            ownerform = OwnerEditForm(request.POST)
            ownerform.username = owner.username
            ownerform.ownertype = owner.ownertype
            
        if 'officialcontactprefix' in request.POST:
            ownerform.officialcontactprefix = request.POST['officialcontactprefix']
        if not ownerform.is_valid():
            passedvalidation = False
            
        for i in xrange(1, int(individualcount)+1):
            individualform = IndividualForm(request.POST, prefix='i'+str(i))
            individualforms.append(individualform)
            if not individualform.is_valid():
                passedvalidation = False
        
        if admin == True:
            ownertype = request.POST['ownertype']
        if admin == False:
            ownertype = owner.ownertype.pk
            
        if int(individualcount) > 1 and str(ownertype) == str(2):
            passedvalidation = False
            ownerform.customerror = "An individual owner share can only have one individual associated with the account"
            
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
            if 'officialcontactprefix' in request.POST:
                owner.officialcontact = findparentinstance(individualforms, request.POST['officialcontactprefix'])
            else:
                individuals = Individual.objects.filter(owner=owner)
                if individuals:
                    owner.officialcontact = individuals[0]
                else:
                    owner.officialcontact = None
            owner.save()
            
            return HttpResponseRedirect('/owners/' + str(owner.username) + '/edit/')

@login_required
def addindividual(request):
    prefix = request.GET['prefix']
    individualform = IndividualForm(prefix='i'+str(prefix))
    
    return render_to_response('owners/individual.html', {'individualform':individualform})

@login_required
def ownersearch(request):
    querystring, searchfield = searchcriteria(request.GET)
    
    if searchfield == 'number':
        query = Q(username=querystring)
    elif searchfield == 'contact':
        query = Q(officialcontact__firstname__contains=querystring) | Q(officialcontact__lastname__contains=querystring)
    else:
        query = Q()
        
    owners = Owner.objects.filter(query)

    form = OwnerSearchForm(initial={'searchfield':searchfield, 'querystring':querystring})
    return render_to_response('owners/search.html', {'owners':owners, 'form':form})
