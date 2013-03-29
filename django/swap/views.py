from django.http import HttpResponse
import datetime

def index(request):
    return HttpResponse("Hi! This is being returned by the 'index' view!")