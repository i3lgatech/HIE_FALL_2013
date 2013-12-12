# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models

class Patient(models.Model):
    patientid = models.IntegerField(primary_key=True)
    password = models.CharField(max_length=45L, blank=True)
    sex = models.CharField(max_length=1L, blank=True)
    first_name = models.CharField(max_length=100L, blank=True)
    last_name = models.CharField(max_length=100L, blank=True)
    greenway_id = models.CharField(max_length=45L, blank=True)
    class Meta:
        db_table = 'patient'
        
class Physician(models.Model):
    physicianid = models.IntegerField(primary_key=True)
    given_name = models.CharField(max_length=100L, blank=True)
    last_name = models.CharField(max_length=100L, blank=True)
    greenway_id = models.CharField(max_length=45L, blank=True)
    greenway_username = models.CharField(max_length=100L, blank=True)
    class Meta:
        db_table = 'physician'

class Activity(models.Model):
    activityid = models.IntegerField(primary_key=True, db_column='activityID') # Field name made lowercase.
    patientid = models.ForeignKey('Patient', db_column='patientID') # Field name made lowercase.
    duration = models.FloatField(null=True, blank=True)
    start_time = models.DateTimeField(null=True, blank=True)
    type = models.IntegerField(null=True, blank=True)
    confidence = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'activity'

class Steps(models.Model):
    stepid = models.IntegerField(primary_key=True, db_column='stepID') # Field name made lowercase.
    patientid = models.ForeignKey('Patient', db_column='patientID') # Field name made lowercase.
    number_steps = models.IntegerField(null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = 'steps'

class Food(models.Model):
    foodid = models.IntegerField(primary_key=True, db_column='foodID') # Field name made lowercase.
    calories = models.IntegerField(null=True, blank=True)
    food_name = models.CharField(max_length=100L, blank=True)
    class Meta:
        db_table = 'food'

class Meal(models.Model):
    mealid = models.IntegerField(db_column='mealID') # Field name made lowercase.
    foodid = models.ForeignKey(Food, db_column='foodID') # Field name made lowercase.
    class Meta:
        db_table = 'meal'

class Intake(models.Model):
    patientid = models.ForeignKey('Patient', db_column='patientID') # Field name made lowercase.
    mealid = models.ForeignKey('Meal', db_column='mealID') # Field name made lowercase.
    score = models.FloatField(null=True, blank=True)
    desired_score = models.FloatField(null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True)
    category = models.CharField(max_length=45L, blank=True)
    class Meta:
        db_table = 'intake'



