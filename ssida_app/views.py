from django.shortcuts import render
from django.http import HttpResponse

from .models import Greeting, LiveData

# Create your views here.
def index(request):
    return render(request, 'index.html')

def rawData(request):
    return render(request, 'rawdata.html')

def storedData(request):
    return render(request, 'storeddata.html')


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})

