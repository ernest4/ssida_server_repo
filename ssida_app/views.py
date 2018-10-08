from django.shortcuts import render
from django.http import HttpResponse

from .models import Greeting, LiveData

# Create your views here.
def index(request):
    return render(request, 'index.html')

def rawData(request):
    params = request.GET

    #device_id = params['device_id']
    #latitude = params['latitude']
    #longitude = params['longitude']
    #accelerometer_x = params['accelerometer_x']
    #accelerometer_y = params['accelerometer_y']
    #accelerometer_z = params['accelerometer_z']
    #gyroscope_x = params['gyroscope_x']
    #gyroscope_y = params['gyroscope_y']
    #gyroscope_z = params['gyroscope_z']
    #timestamp = params['timestamp']

    return render(request, 'rawdata.html', {'params': params, 'keys': params.keys()})

def storedData(request):
    return render(request, 'storeddata.html')


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})

