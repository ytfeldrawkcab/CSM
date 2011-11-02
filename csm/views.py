from csm.models import *
from csm.forms import *

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required, user_passes_test
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
        return render_to_response('index.html', RequestContext(request, {}))

#owner management
@login_required
def editowner(request, ownerid=None):
    try:
        if request.user.owner and not ownerid:
            ownerid = request.user.owner.username
        elif request.user.owner and ownerid:
            return HttpResponseRedirect('/owners/')
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
            
            if admin == True:
                return HttpResponseRedirect('/owners/' + str(owner.username) + '/edit/')
            else:
                return HttpResponseRedirect('/owners/')

@login_required
def addindividual(request):
    prefix = request.GET['prefix']
    individualform = IndividualForm(prefix='i'+str(prefix))
    
    return render_to_response('owners/individual.html', {'individualform':individualform})

@user_passes_test(lambda u: u.is_staff)
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
    return render_to_response('owners/search.html', RequestContext(request, {'owners':owners, 'form':form}))

#election management
@login_required
def vote(request, electionid):
    election = Election.objects.get(pk=electionid)
    candidates = Candidate.objects.filter(election=election)
    if request.method == 'GET':
        votes = Vote.objects.filter(candidate__election=election)
        voteforms = []
        v = 0
        for candidate in candidates:
            v += 1
            instance = None
            selected = False
            for vote in votes:
                if vote.candidate == candidate:
                    instance = vote
                    selected = True
                    break
                else:
                    instance = None
                    selected = False
            voteform = VoteForm(instance=instance, prefix='v'+str(v), initial={'candidate':candidate.pk, 'selected':selected})
            voteforms.append(voteform)
        
        return render_to_response('elections/vote.html', RequestContext(request, {'voteforms':voteforms, 'election':election, 'candidates':candidates, 'votecount':v}))
    
    else:
        passedvalidation = True
        votecount = request.POST['votecount']
        voteforms = []
        
        selectedcount = 0
        for v in xrange(1, int(votecount)+1):
            voteform = VoteForm(request.POST, prefix='v'+str(v))
            voteforms.append(voteform)
            if 'v'+str(v)+'-selected' in request.POST:
                selectedcount += 1
            if not voteform.is_valid():
                passedvalidation = False
        
        if selectedcount > election.maxchoices:
            passedvalidation = False
        
        if not passedvalidation:
            return render_to_response('elections/vote.html', RequestContext(request, {'voteforms':voteforms, 'election':election, 'candidates':candidates, 'votecount':v}))
            
        else:
            for voteform in voteforms:
                vote = voteform.save(commit=False)
                vote.owner = request.user.owner
                if voteform.cleaned_data['selected']:
                    vote.save()
                elif vote.pk:
                    vote.delete()
            
            return HttpResponseRedirect('/elections/' + str(election.pk))
            
@login_required
def editelection(request, electionid=None):   
    if request.method == 'GET':
        if electionid:
            election = Election.objects.get(pk=electionid)
        else:
            election = None
        
        candidates = Candidate.objects.filter(election=election)
        c = 0
        candidateforms = []
        for candidate in candidates:
            c += 1
            candidateform = CandidateForm(instance=candidate, prefix='c'+str(c))
            candidateforms.append(candidateform)
        
        electionform = ElectionForm(instance=election, initial={'candidatecount':c})
        
        return render_to_response('elections/edit.html', RequestContext(request, {'form':electionform, 'candidateforms':candidateforms}))
    else:
        passedvalidation = True
        candidatecount = request.POST['candidatecount']
        candidateforms = []
        
        electionform = ElectionForm(request.POST)
                    
        for c in xrange(1, int(candidatecount)+1):
            candidateform = CandidateForm(request.POST, prefix='c'+str(c))
            candidateforms.append(candidateform)
            if not candidateform.is_valid():
                passedvalidation = False
            
        if passedvalidation == False:
            return render_to_response('elections/edit.html', RequestContext(request, {'form':electionform, 'candidateforms':candidateforms}))
        
        else:
            election = electionform.save()
            
            for candidateform in candidateforms:
                candidate = candidateform.save(commit=False)
                candidate.election = election
                if candidateform.cleaned_data['delete'] == 0:
                    candidate.save()
                elif candidate.pk:
                    candidate.delete()
            
            return HttpResponseRedirect('/elections/' + str(election.pk))
