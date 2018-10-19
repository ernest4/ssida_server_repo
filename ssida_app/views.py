from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Greeting, LiveData
from django.core import serializers
import csv
from django.utils.encoding import smart_str

# Create your views here.
def index(request):
    return render(request, 'index.html')

def howThisWorks(request):
    return render(request, 'howthisworks.html')

def whatIsSidda(request):
    return render(request, 'whatissidda.html')

def howAnalyticsWorks(request):
    return render(request, 'howanalyticsworks.html')

def ourTeam(request):
    return render(request, 'ourteam.html')

def showRawData(request):
    # QuerySet.values() returns a list of dictionaries representing the records
    live_data = LiveData.objects.all().order_by('id').reverse()[:8].values()
    keys = live_data[0].keys()

    return render(request, 'livedata.html', {'recordDicts': live_data,'keys':keys})

def showStoredData(request):
    return render(request, 'storeddata.html')


@require_http_methods(['GET'])
def getRawData(request):
    params = request.GET

    if len(params)!=0:
        rows = int(params['rows'])

        live_data = LiveData.objects.all().order_by('id').reverse()[:rows] #ORM query
        #live_data = LiveData.objects.raw('SELECT * FROM ssida_app_livedata') #raw SQL query
    else:
        live_data = {}

    live_data = serializers.serialize('json', live_data) #convert QuerySet to JSON
    return HttpResponse(live_data, content_type='application/json')


@require_http_methods(['GET'])
def getStoredData(request):
    params = request.GET

    # live_data = LiveData.objects.raw('SELECT * FROM ssida_app_livedata') #raw SQL query

    if len(params) != 0:
        rows = params['rows']
        if rows == 'all':
            live_data = LiveData.objects.all().order_by('id').reverse()
        else:
            rows = int(rows)
            live_data = LiveData.objects.all().order_by('id').reverse()[:rows]  # ORM query
    else:
        live_data = {}

    live_data = serializers.serialize('json', live_data)  # convert QuerySet to JSON
    return HttpResponse(live_data, content_type='application/json')


def downloadData(request):
    params = request.GET

    if len(params) != 0:
        rows = params['rows']
        if rows == 'all':
            live_data = LiveData.objects.all().order_by('id').reverse()
        else:
            rows = int(rows)
            live_data = LiveData.objects.all().order_by('id').reverse()[:rows]  # ORM query

        # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="data.csv"'

        #writer = csv.writer(response)
        #writer.writerow(['Rows', 'Foo', 'Bar', 'Baz'])
        #writer.writerow([rows, 'A', 'B', 'C', '"Testing"', "Here's a quote"])

        writer = csv.writer(response, csv.excel)
        response.write(u'\ufeff'.encode('utf8'))

        # write the headers
        writer.writerow([
            smart_str(u"device_id"),
            smart_str(u"latitude"),
            smart_str(u"longitude"),
            smart_str(u"accelerometer_x"),
            smart_str(u"accelerometer_y"),
            smart_str(u"accelerometer_z"),
            smart_str(u"gyroscope_x"),
            smart_str(u"gyroscope_y"),
            smart_str(u"gyroscope_z"),
            smart_str(u"timestamp"),
        ])

        # itterate over the data from database
        for row in live_data:
            writer.writerow([
                smart_str(row.id),
                smart_str(row.latitude),
                smart_str(row.longitude),
                smart_str(row.accelerometer_x),
                smart_str(row.accelerometer_y),
                smart_str(row.accelerometer_z),
                smart_str(row.gyroscope_x),
                smart_str(row.gyroscope_y),
                smart_str(row.gyroscope_z),
                smart_str(row.timestamp),
            ])

    return response


@require_http_methods(['GET','POST'])
def setRawData(request):
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


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})

