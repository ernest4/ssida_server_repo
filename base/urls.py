from django.conf.urls import include, url
from django.urls import path

from django.contrib import admin
admin.autodiscover()

import ssida_app.views

# Examples:
# url(r'^$', 'base.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', ssida_app.views.index, name='index'),
    url(r'^db', ssida_app.views.db, name='db'),
    path('admin/', admin.site.urls),
]
