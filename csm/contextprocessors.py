from csm.models import *
from datetime import datetime

def user(request):
    if hasattr(request, 'user'):
        return {'user':request.user }
    return {}

def openelections(request):
    openelections = Election.objects.filter(beginvoting__lte=datetime.today).filter(endvoting__gte=datetime.today)
    return {'openelections':openelections}
