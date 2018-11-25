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
from ssida_app.algorithm_offline_data import compute_geo_score

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
    last_run_value = request.session.get('lastRunRowCount', 8)
    last_run_device_id = request.session.get('lastRunDeviceID', 'all')
    last_run_date_time_old = request.session.get('lastRunDateTimeOld', 'none')
    last_run_date_time_new = request.session.get('lastRunDateTimeNew', 'none')

    # Set session as modified to force data updates/cookie to be saved.
    # (only truly necessary if updating internal data such as
    # request.session['lastRunValue']['someOtherValue'] = ...)
    request.session.modified = True

    context = {'last_run_value': last_run_value,
               'last_run_device_id': last_run_device_id,
               'last_run_date_time_old': last_run_date_time_old,
               'last_run_date_time_new': last_run_date_time_new}

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


def getDataFromDB(rows, deviceids, datetimeold, datetimenew):
    # live_data = LiveData.objects.raw('SELECT * FROM ssida_app_livedata') #raw SQL query

    allStoredData = LiveData.objects.all()
    totalDataCount = allStoredData.count()

    allStoredDataRevOrd = allStoredData.order_by('id').reverse()

    #filter by device_id
    if deviceids != 'all':
        deviceidsFullName = "com.google.android.gms.iid.InstanceID@" + deviceids
        allStoredDataRevOrd = allStoredDataRevOrd.filter(device_id=deviceidsFullName)

    #filter by selecting rows newer than chosend date
    if datetimeold != 'none':
        allStoredDataRevOrd = allStoredDataRevOrd.filter(timestamp__gt=datetimeold)

    #filter by selecting rows older than chosen date
    if datetimenew != 'none':
        allStoredDataRevOrd = allStoredDataRevOrd.filter(timestamp__lt=datetimenew)

    #filter by number of rows desired
    if rows != 'all':
        rows = int(rows)
        allStoredDataRevOrd = allStoredDataRevOrd[:rows]

        # allLiveData.objects.filter(year_published__gt=1990) \
        #            .exclude(author='Richard Dawkins') \
        #                .order_by('author', '- year_published')
    return allStoredDataRevOrd, totalDataCount


@require_http_methods(['GET'])
def getStoredData(request):
    params = request.GET

    rows = params['rows']
    deviceids = params['device_ids']
    datetimeold = params['date_time_old']
    datetimenew = params['date_time_new']

    # Set a session value
    request.session['lastRunRowCount'] = rows
    request.session['lastRunDeviceID'] = deviceids
    request.session['lastRunDateTimeOld'] = datetimeold
    request.session['lastRunDateTimeNew'] = datetimenew

    # Set session as modified to force data updates/cookie to be saved.
    # (only truly necessary if updating internal data such as
    # request.session['lastRunValue']['someOtherValue'] = ...)
    request.session.modified = True

    selection, totalDataCount = getDataFromDB(rows=rows,
                                              deviceids=deviceids,
                                              datetimeold=datetimeold,
                                              datetimenew=datetimenew)

    selectionCount = selection.count()

    support_data = { 'totalDataCount': totalDataCount,
                     'selectionCount': selectionCount,
                     'selection': selection }

    # convert QuerySet to JSON
    live_data = serializers.serialize('json', selection)

    return HttpResponse(live_data, content_type='application/json')


def downloadData(request):
    params = request.GET

    rows = params['rows']
    deviceids = params['device_ids']
    datetimeold = params['date_time_old']
    datetimenew = params['date_time_new']

    # Set a session value
    request.session['lastRunRowCount'] = rows
    request.session['lastRunDeviceID'] = deviceids
    request.session['lastRunDateTimeOld'] = datetimeold
    request.session['lastRunDateTimeNew'] = datetimenew

    # Set session as modified to force data updates/cookie to be saved.
    # (only truly necessary if updating internal data such as
    # request.session['lastRunValue']['someOtherValue'] = ...)
    request.session.modified = True

    live_data, live_data_count = getDataFromDB(rows=rows,
                                               deviceids=deviceids,
                                               datetimeold=datetimeold,
                                               datetimenew=datetimenew)

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



def updateMapTable(request):
    is_successful = compute_geo_score(begin_timestamp="2018-11-18 14:20:00.000000+00:00", end_timestamp="2018-11-18 15:30:00.000000+00:00")

    return render(request, 'updatetmaptable.html', {'isSuccessful': is_successful})

