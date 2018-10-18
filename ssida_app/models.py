from django.db import models

# Create your models here.
class Greeting(models.Model):
    when = models.DateTimeField('date created', auto_now_add=True)


class LiveData(models.Model):
    device_id = models.CharField(max_length=50)
    latitude = models.DecimalField(max_digits=9,decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    accelerometer_x = models.FloatField()
    accelerometer_y = models.FloatField()
    accelerometer_z = models.FloatField()
    gyroscope_x = models.FloatField(null=True)
    gyroscope_y = models.FloatField(null=True)
    gyroscope_z = models.FloatField(null=True)
    timestamp = models.DateTimeField('time of generation', auto_now=True)

    def __str__(self):
        return self.device_id
    
    class Meta():
        verbose_name_plural = "Live Positioning Data"
        indexes = [
            models.Index(fields=['device_id']),
            models.Index(fields=['latitude','longitude'])
        ]
