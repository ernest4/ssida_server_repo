from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Greeting, LiveData, ScoreData
from django.core import serializers
import csv
from django.utils.encoding import smart_str
from django.contrib.auth.decorators import login_required
import json

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


def agreeToCookie(request):
    params = request.GET
    setCookie = params['allowCookie']

    # getCookie, if it doesn't exist set it to False by default
    allowCookie = request.session.get('allowCookie', False)

    if setCookie == 'true':
        # Set a session value
        allowCookie = request.session['allowCookie'] = True

    # Set session as modified to force data updates/cookie to be saved.
    # (only truly necessary if updating internal data such as
    # request.session['lastRunValue']['someOtherValue'] = ...)
    request.session.modified = True

    cookiePermision = {'allowCookie': allowCookie}

    return JsonResponse(cookiePermision)


def showRawData(request):
    # QuerySet.values() returns a list of dictionaries representing the records
    live_data = LiveData.objects.all().order_by('id').reverse()[:8].values()
    keys = live_data[0].keys()

    return render(request, 'livedata.html', {'recordDicts': live_data,'keys':keys})

#@login_required
def showStoredData(request):
    # Get a session value, setting a default if it is not present (8)
    last_run_value = request.session.get('lastRunValue', 8)

    # Set session as modified to force data updates/cookie to be saved.
    # (only truly necessary if updating internal data such as
    # request.session['lastRunValue']['someOtherValue'] = ...)
    request.session.modified = True

    context = {'last_run_value': last_run_value}

    return render(request, 'storeddata.html', context=context)


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

        # Set a session value
        request.session['lastRunValue'] = rows

        # Set session as modified to force data updates/cookie to be saved.
        # (only truly necessary if updating internal data such as
        # request.session['lastRunValue']['someOtherValue'] = ...)
        request.session.modified = True

        allLiveData = LiveData.objects.all()
        totalDataCount = allLiveData.count()

        if rows == 'all':
            selection = allLiveData.order_by('id').reverse()
        else:
            rows = int(rows)
            selection = allLiveData.order_by('id').reverse()[:rows]  # ORM query

    selectionCount = selection.count()

    support_data = { 'totalDataCount': totalDataCount,
                     'selectionCount': selectionCount,
                     'selection': selection }

    # convert QuerySet to JSON
    live_data = serializers.serialize('json', selection)

    return HttpResponse(live_data, content_type='application/json')


def downloadData(request):
    params = request.GET

    if len(params) != 0:
        rows = params['rows']

        # Set a session value
        request.session['lastRunValue'] = rows

        # Set session as modified to force data updates/cookie to be saved.
        # (only truly necessary if updating internal data such as
        # request.session['lastRunValue']['someOtherValue'] = ...)
        request.session.modified = True

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


def getMapData(request):
    allMapData = ScoreData.objects.all()

    # convert QuerySet to JSON
    map_data = serializers.serialize('json', allMapData)

    return HttpResponse(map_data, content_type='application/json')


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})

