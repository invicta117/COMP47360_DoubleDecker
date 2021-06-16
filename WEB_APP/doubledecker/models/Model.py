

# import django models module
from django.db import models

'''
According the datafile we got, I design the model. 
But not sure how translate the datafile to a sql file and put it on the database
'''
class RTTrips(models.Model):
    tripId = models.IntegerField(db_column='tripId', unique=True, primary_key=True)
    dataSource = models.CharField(db_column='dataSource', max_length=200)
    dayOfService = models.DateTimeField(db_column='dayOfService', blank=True, null=True)
    lineId = models.CharField(db_column='lineId', max_length=50)
    routeId = models.CharField(db_column='routeId',max_length=50)
    direction = models.CharField(db_column='direction', max_length=40)
    plannedTime_Arr = models.TimeField(db_column='plannedTime_Arr')
    plannedTime_Dep = models.TimeField(db_column='plannedTime_Dep')
    actualTime_arr = models.TimeField(db_column='actualTime_arr')
    actualTime_Dep = models.TimeField(db_column='actualTime_Dep')
    basin = models.CharField(db_column='basin', max_length=100)
    tenderLot = models.CharField(db_column='tenderLot', max_length=100)
    suppressed = models.CharField(db_column='suppressed')
    justificationId = models.IntegerField(db_column='justificationId', blank=True, null=True)
    lastUpdate = models.DateField(db_column='lastUpdate')
    note = models.CharField(db_column='note', max_length=50)

    class Meta:
        managed = False
        db_table = 'RT_Trips'


class RT_LeaveTimes(models.Model):
    tripId = models.IntegerField(db_column='tripId', unique=True, primary_key=True)
    dataSource = models.CharField(db_column='dataSource',max_length=200)
    dayOfService = models.DateTimeField(db_column='dayOfService', blank=True, null=True)
    progrNumber = models.IntegerField(db_column='progrNumber')
    stopId = models.IntegerField(db_column='stopId', max_length=50)
    plannedTime_Arr = models.TimeField(db_column='plannedTime_Arr')
    plannedTime_Dep = models.TimeField(db_column='plannedTime_Dep')
    actualTime_arr = models.TimeField(db_column='actualTime_arr')
    actualTime_Dep = models.TimeField(db_column='actualTime_Dep')
    vehicleId = models.IntegerField(db_column='vehicleId')
    passengers = models.IntegerField(db_column='passengers', max_length=100)
    passengersIn = models.IntegerField(db_column='passengersIn')
    passengersOut = models.IntegerField(db_column='passengersOut')
    distance = models.IntegerField(db_column='distance')
    suppressed = models.CharField(db_column='suppressed')
    justificationId = models.IntegerField(db_column='justificationId', blank=True, null=True)
    lastUpdate = models.DateField(db_column='lastUpdate')
    note = models.CharField(db_column='note', max_length=50)

    class Meta:
        managed = False
        db_table = 'RT_LeaveTimes'


# Maybe we need to scrap the weather data to train the model.
class Weather(models.Model):
    lat = models.FloatField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)
    temp = models.FloatField(blank=True, null=True)
    feels_like = models.FloatField(blank=True, null=True)
    temp_min = models.FloatField(db_column='temp_Min',blank=True, null=True)
    temp_max = models.FloatField(db_column='temp_Max', blank=True, null=True)
    pressure = models.FloatField(blank=True, null=True)
    humidity = models.IntegerField(blank=True, null=True)
    wind_speed = models.FloatField(blank=True, null=True)
    wind_deg = models.IntegerField(blank=True, null=True)
    rain_1h = models.TextField(blank=True, null=True)
    rain_3h = models.TextField(blank=True, null=True)
    snow_1h = models.TextField(blank=True, null=True)
    snow_3h = models.TextField(blank=True, null=True)
    clouds_all = models.IntegerField(blank=True, null=True)
    weather_id = models.IntegerField(blank=True, null=True, primary_key=True)
    weather_main = models.TextField(blank=True, null=True)
    weather_description = models.TextField(blank=True, null=True)
    weather_icon = models.TextField(blank=True, null=True)
    sunrise = models.DateTimeField(blank=True, null=True)
    sunset = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'weather'
