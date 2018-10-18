from django.conf.urls import include, url
from django.urls import path

from django.contrib import admin
admin.autodiscover()


import ssida_app.views

urlpatterns = [
    #pages
    path('', ssida_app.views.index, name=''),
    path('index', ssida_app.views.index, name='index'),
    path('livedata',ssida_app.views.showRawData,name='showrawdata'),
    path('storeddata', ssida_app.views.showStoredData, name='storeddata'),
    path('howthisworks', ssida_app.views.howThisWorks, name='howthisworks'),
    path('whatissidda', ssida_app.views.whatIsSidda, name='whatissidda'),
    path('ourteam', ssida_app.views.ourTeam, name='ourTeam'),
    path('howanalyticsworks', ssida_app.views.howAnalyticsWorks, name='howanalyticsworks'),

    #apis
    path('rawdata', ssida_app.views.setRawData, name='rawdata'),
    path('getrawdata', ssida_app.views.getRawData, name='getrawdata'),
    path('getstoreddata', ssida_app.views.getStoredData, name='getstoreddata'),

    path('db', ssida_app.views.db, name='db'),
    path('admin/', admin.site.urls),
]
