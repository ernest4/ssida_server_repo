from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from .models import Greeting, LiveData

# Create your views here.
def index(request):
    return render(request, 'index.html')

def showRawData(request):
    #live_data = LiveData.objects.all().values()
    live_data = LiveData.objects.latest('timestamp').values()
    keys = dict(list(live_data)[0]).keys()

    return render(request, 'livedata.html', {'params': live_data,'keys':keys})

@require_http_methods(['GET','POST'])
def rawData(request):
    params = request.GET
    live_data = LiveData()
    if len(params)!=0:
        print("getting data")
        live_data.device_id = params.get('device_id')
        live_data.latitude = params.get('latitude')
        live_data.longitude = params.get('longitude')
        live_data.accelerometer_x = params.get('accelerometer_x')
        live_data.accelerometer_y = params.get('accelerometer_y')
        live_data.accelerometer_z = params.get('accelerometer_z')
        live_data.gyroscope_x = params.get('gyroscope_x')
        live_data.gyroscope_y = params.get('gyroscope_y')
        live_data.gyroscope_z = params.get('gyroscope_z')
        live_data.timestamp = params.get('timestamp')
        live_data.save()
    return render(request, 'livedata.html', {'params': params, 'keys': params.keys()})

def storedData(request):
    return render(request, 'storeddata.html')


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})

