from django.contrib import admin
from .models import LiveData, ScoreData

# Register your models here.
admin.site.register(LiveData)
admin.site.register(ScoreData)
