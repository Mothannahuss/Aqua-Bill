from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid
import secrets
import datetime
from django.db.models import Sum
import datetime 


# Create your models here.

class User(AbstractUser):
    pass


"""sumary_line
    Device Model
    Stores sensor information as follows:
    last_update: timestamp of last update on the device
    current_read: the current daily total reading of water
    month_read: the current monthly total reading of water
"""
class Device(models.Model):
    last_update = models.DateTimeField(auto_now=True)
    current_read = models.FloatField(null=True, default=0)
    current_month = models.CharField(max_length=9)
    month_read = models.FloatField(null=True, default=0)
    api_key = models.CharField(max_length=256, unique=True, default=uuid.uuid4)



    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self._last_reading = self.current_read
        self._update = self.last_update

    def save(self, *args, **kwargs):
        # Check for api, month values initialization
        if not self.api_key:
            self.api_key = uuid.uuid4().hex
        if not self.last_update:
            self.last_update = datetime.datetime.now()
        if not self.current_month:
            self.current_month = self.last_update.strftime("%B")


        date = datetime.datetime.now()
        month_name = date.strftime("%B")

        # Checking weather we entered a new month
        if month_name != self.current_month:
            self.month_read = 0
            self.current_month = month_name
        else:
            self.month_read = self._last_reading if self._last_reading > self.current_read else self.current_read

        # Creating a new daily archive record if we entered a new day
        if self._update and str(date.date()) != str(self._update.date()):
            total_reading = self._last_reading
            self.current_read = 0
            daily = DailyArchive(
                device=self, date=self._update.date(),
                day=self._update.day, 
                total_reading=total_reading
            )
            daily.save()
        
        
        super(Device, self).save(*args, **kwargs)
        self._last_reading = self.current_read
        self._update = self.last_update



"""sumary_line
DailyArchive model
Used to store daily records of device models
When we enter a new day, a new archive will be created from the device's save function
device: a reference to the device that owns the archive
date: the date of the new archive
month: the month of the new archive
day: the day of the new archive
total_reading: the total amount of water read by the device in the given day
"""

class DailyArchive(models.Model):
        device = models.ForeignKey(Device, models.SET_NULL, null=True, blank=True)
        date = models.DateTimeField()
        month = models.CharField(max_length=9, null=True)
        day = models.IntegerField(null=True, default=0)
        total_reading = models.FloatField(null=False, default=0)

        def save(self, *args, **kwargs):
            if not self.date:
                self.date = device.last_update if device else datetime.datetime.now()
                self.month = self.date.month.strftime("%B")
                self.day = self.date.day
            

            current_date = datetime.datetime.now()
            month = self.date.strftime("%B")

            # In case we enter a new month, we need to simplify the archives
            # We aggregate the reading of the past month and make a monthly archive record
            if self.date and month != self.date.strftime("%B") and self.device:
                total = DailyArchive.objects.filter(device=self.device).aggregate(total = Sum("total_reading"))['total']
                monthly = MonthlyArchive(self.device, month=month, total_reading=total)
                monthly.save()
            super(DailyArchive, self).save(*args, **kwargs)

class MonthlyArchive(models.Model):
    device = models.ForeignKey(Device, models.SET_NULL, null=True, blank=True)
    month = models.CharField(max_length=9, null=True)
    total_reading = models.FloatField(null=False)


    def save(self, *args, **kwargs):
        if not self.month:
            self.month = device.last_update if device else datetime.datetime.now()
        

        if device:
            DailyArchive.objects.filter(device = self.device, month=self.month).delete()
        super(MonthlyArchive, self).save(*args, **kwargs)



"""sumary_line
Unit model
attributes:
device: a foreign key representing the device that is installed in the unit
number: an integer representing the unit number
url: a string representing the url that points to the dashboard that contains unit's information
"""
class Unit(models.Model):
    device = models.ForeignKey(Device, models.SET_NULL, null=True, blank=True)
    number = models.IntegerField(default=0)
    url = models.URLField()
    quality_level = models.FloatField(default=0.4)


    def save(self, *args, **kwargs):
        if not self.url:
            self.url = "http://127.0.0.1:8000/" + str(self.number)

        super(Unit, self).save(*args, **kwargs)

        

