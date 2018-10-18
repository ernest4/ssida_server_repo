from django.conf.urls import include, url
from django.urls import path

from django.contrib import admin
admin.autodiscover()


import ssida_app.views

# Examples:
# url(r'^$', 'base.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    #pages
    url(r'^$', ssida_app.views.index, name=''),
    url('index', ssida_app.views.index, name='index'),
    url('livedata',ssida_app.views.showRawData,name='showrawdata'),
    url('storeddata', ssida_app.views.showStoredData, name='storeddata'),
    url('howthisworks', ssida_app.views.howThisWorks, name='howthisworks'),
    url('whatissidda', ssida_app.views.whatIsSidda, name='whatissidda'),
    url('ourteam', ssida_app.views.ourTeam, name='ourTeam'),
    url('howanalyticsworks', ssida_app.views.howAnalyticsWorks, name='howanalyticsworks'),

    #apis
    url('rawdata', ssida_app.views.setRawData, name='rawdata'),
    url('getrawdata', ssida_app.views.getRawData, name='getrawdata'),

    url(r'^db', ssida_app.views.db, name='db'),
    path('admin/', admin.site.urls),
]
