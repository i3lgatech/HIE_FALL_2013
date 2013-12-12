from django.http import HttpResponse
#from django.core import serializers
import json
from models import Activity
from models import Patient
from models import Steps
from datetime import datetime
from pytz import timezone
import vik

from django.db import models
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def addActivity(request):
    #here take the json out of the request and create an Activity object for each one,
    #and save it to the database
    meth = "" #Meth is bad shane...
    
    #test method - create test JSON file (WORKING)
    
    vik.alertFunc()
    
    lastActivityId = -1
    try:
        # get
        lastActivityObject = Activity.objects.latest('activityid')
        lastActivityId = lastActivityObject.activityid
    except Activity.DoesNotExist:
        # create
        lastActivityId = 1    
        
    #1 object
    #response = json.dumps({'confidence': 1L, 'start_time': "2013-11-06 00:00:00.000", 'duration': durationquant, 'type': 1L, 'activityid': 1L})
    # 2 objects
    #response = json.dumps([{'confidence': 1, 'start_time': "2013-11-06 00:00:00.000", 'duration': durationquant, 'type': 1, 'activityid': 1L},{'confidence': 3, 'start_time': "2013-11-02 00:00:00.000", 'duration': durationquant, 'type': 2, 'activityid': 1L}])
    #full json file
    response = json.dumps([
  {
    "confidence" : 2,
    "type" : 3,
    "start_time" : "2013-11-07 00:00:00.000",
    "duration" : 21388.32,
    'activityid': 1L
  },
  {
    "confidence" : 2,
    "type" : 3,
    "start_time" : "2013-11-07 05:56:28.323",
    "duration" : 4,
    'activityid': 1L
  },
  {
    "confidence" : 2,
    "type" : 3,
    "start_time" : "2013-11-07 05:56:32.323",
    "duration" : 7.036205,
    'activityid': 1L
  },
  {
    "confidence" : 2,
    "type" : 3,
    "start_time" : "2013-11-07 05:56:39.359",
    "duration" : 888.2421,
    'activityid': 1L
  },
  {
    "confidence" : 2,
    "type" : 3,
    "start_time" : "2013-11-07 06:11:27.601",
    "duration" : 4,
    'activityid': 1L
  },
  {
    "confidence" : 2,
    "type" : 3,
    "start_time" : "2013-11-07 06:11:31.601",
    "duration" : 5.812803,
    'activityid': 1L
  },
  {
    "confidence" : 2,
    "type" : 3,
    "start_time" : "2013-11-07 06:11:37.414",
    "duration" : 891.5458,
    'activityid': 1L
  },
  {
    "confidence" : 2,
    "type" : 3,
    "start_time" : "2013-11-07 06:26:28.959",
    "duration" : 4,
    'activityid': 1L
  },
  {
    "confidence" : 2,
    "type" : 3,
    "start_time" : "2013-11-07 06:26:32.959",
    "duration" : 5.505439,
    'activityid': 1L
  },
  {
    "confidence" : 2,
    "type" : 3,
    "start_time" : "2013-11-07 06:26:38.465",
    "duration" : 2378.442,
    'activityid': 1L
  },
  {
    "confidence" : 2,
    "type" : 3,
    "start_time" : "2013-11-07 07:06:16.907",
    "duration" : 4,
    'activityid': 1L
  },
  {
    "confidence" : 2,
    "type" : 3,
    "start_time" : "2013-11-07 07:06:20.907",
    "duration" : 39.12969,
    'activityid': 1L
  },
  {
    "confidence" : 2,
    "type" : 3,
    "start_time" : "2013-11-07 07:07:00.037",
    "duration" : 4,
    'activityid': 1L
  },
  {
    "confidence" : 2,
    "type" : 3,
    "start_time" : "2013-11-07 07:07:04.037",
    "duration" : 0.305856,
    'activityid': 1L
  },
  {
    "confidence" : 2,
    "type" : 3,
    "start_time" : "2013-11-07 07:07:04.343",
    "duration" : 17.71741,
    'activityid': 1L
  },
  {
    "confidence" : 2,
    "type" : 3,
    "start_time" : "2013-11-07 07:07:22.060",
    "duration" : 4,
    'activityid': 1L
  },
  {
    "confidence" : 1,
    "type" : 3,
    "start_time" : "2013-11-07 07:07:26.060",
    "duration" : 0.611779,
    'activityid': 1L
  },
  {
    "confidence" : 1,
    "type" : 3,
    "start_time" : "2013-11-07 07:07:26.672",
    "duration" : 29.64928,
    'activityid': 1L
  },
  {
    "confidence" : 2,
    "type" : 3,
    "start_time" : "2013-11-07 07:07:56.321",
    "duration" : 4,
    'activityid': 1L
  },
  {
    "confidence" : 2,
    "type" : 3,
    "start_time" : "2013-11-07 07:08:00.321",
    "duration" : 52.46044,
    'activityid': 1L
  },
  {
    "confidence" : 2,
    "type" : 3,
    "start_time" : "2013-11-07 07:08:52.782",
    "duration" : 4,
    'activityid': 1L
  },
  {
    "confidence" : 2,
    "type" : 3,
    "start_time" : "2013-11-07 07:08:56.782",
    "duration" : 106.4373,
    'activityid': 1L
  },
  {
    "confidence" : 2,
    "type" : 3,
    "start_time" : "2013-11-07 07:10:43.219",
    "duration" : 4,
    'activityid': 1L
  },
  {
    "confidence" : 2,
    "type" : 3,
    "start_time" : "2013-11-07 07:10:47.219",
    "duration" : 1275.257,
    'activityid': 1L
  },
  {
    "confidence" : 2,
    "type" : 3,
    "start_time" : "2013-11-07 07:32:02.476",
    "duration" : 4,
    'activityid': 1L
  },
  {
    "confidence" : 2,
    "type" : 3,
    "start_time" : "2013-11-07 07:32:06.476",
    "duration" : 92.37314,
    'activityid': 1L
  },
  {
    "confidence" : 2,
    "type" : 3,
    "start_time" : "2013-11-07 07:33:38.849",
    "duration" : 4,
    'activityid': 1L
  },
  {
    "confidence" : 2,
    "type" : 3,
    "start_time" : "2013-11-07 07:33:42.849",
    "duration" : 186.2058,
    'activityid': 1L
  },
  {
    "confidence" : 2,
    "type" : 3,
    "start_time" : "2013-11-07 07:36:49.055",
    "duration" : 4,
    'activityid': 1L
  },
  {
    "confidence" : 2,
    "type" : 3,
    "start_time" : "2013-11-07 07:36:53.055",
    "duration" : 358.3061,
    'activityid': 1L
  },
  {
    "confidence" : 0,
    "type" : 3,
    "start_time" : "2013-11-07 07:42:51.361",
    "duration" : 4,
    'activityid': 1L
  }
])
    
    #test method - load JSON file into database (NOT TESTED)
    #data = json.loads(response, cls=ConcatJSONDecoder)
    #data = json.loads(response)
    #actid = durationquant + 1
    #output = 0
    #for actobj in data:
    #    newactivity = create_or_update_and_get(Activity, actobj, actid)
    #    actid = actid + 1
    #    output = output + newactivity.confidence
    #    newactivity.save()
      
    
    
    if request.method == 'GET':
        #test code - create a new Activity and save it to the database
        #testPatient = Patient.objects.get(pk=1)
        #durationObject = Activity.objects.latest('activityid')
        #durationquant = durationObject.activityid
        #newActivity = Activity(patientid = testPatient, duration = durationquant, type = 1, confidence = 1)#start_time
        #newActivity.save()
        
        
        #testActivity = Activity.objects.get(activityid=1)
        
        
        #test code to parse JSON - not working
        #testText = ""
        #for deserialized_object in serializers.deserialize("json", testJSONActivity):
            #if object_should_be_save:(deserialized_object)
        #    deserialized_object.save()
        #testArray = json.loads(testJSONActivity)
        #testText = testActivity.duration
        #meth = "via a GET - %s" % Activity.objects.filter(activityid = 1).values()
        
        #meth = "via a GET - %s" % newactivity.duration
        #meth = "via a GET - %s" % output
        meth = "via a GET test"
    elif request.method == 'POST':
        #here, get the JSON array of activity objects from
        #request.POST['activity']
        data = json.loads(request.POST['activity'])
        actid = lastActivityId + 1
        for actobj in data:
            newactivity = create_or_update_and_get(Activity, actobj, actid)
            actid = actid + 1
            try:
                newactivity.save()
            except Exception as e:
                print("couldn't save...")
        #newActivity = create_or_update_and_get(Activity, data)
        #newActivity = Activity(patientid = 1, duration = 1234, type = 1, confidence = 1)#start_time
        #newActivity.save()
        #testActivity = Activity.objects.get(activityid=1)
        #, understand what this looks like and convert to array if needed
        #testText = testActivity.duration
        #meth = "via a POST - %s" % newActivity
        meth = "via a POST - %s" % data
    return HttpResponse("true")

@csrf_exempt
def addSteps(request):
    #step object separated by days
    
    #find the latest date and largest stepid in the DB
    try:
        # get
        lastStepIdObject = Steps.objects.latest('stepid')
        lastStepId = lastStepIdObject.stepid
        lastStepIdObject.delete()
    except Steps.DoesNotExist:
        # create
        lastStepId = 0
    
    #TEST CODE - DUMMY STEPS DATA
    stepsResponse = json.dumps([
                           {
                            "number_steps" : 32,
                            "date" : "2013-11-11 23:59:59.000",
                            "stepid": 1L
                            },
                           {
                            "number_steps" : 456,
                            "date" : "2013-11-12 23:59:59.000",
                            "stepid": 1L
                            }])
    
    meth1 = ""
    #TEST CODE - GET METHOD
    if request.method == 'GET':
        
        

        stepId = lastStepId + 1
        test = ""
        for stepObject in stepsData:
            #create an object with the same stepID and patientID
            #add the date /time of the new JSON and add the steps of the JSON object and the DB object
            newStepObject = create_or_update_and_get_steps(Steps, stepObject, stepId)
            stepId = stepId + 1
            newStepObject.save()
        meth1 = "via a GET - %s" % test
    elif request.method == 'POST':
        #here, get the JSON array of step objects, may need to update step objects that are already in the DB
        #request.POST['steps']
                #here, get the JSON array of activity objects from
        #request.POST['activity']
        stepsData = json.loads(request.POST['steps'])
        stepId = lastStepId + 1
        for stepObject in stepsData:
            #create an object with the same stepID and patientID
            #add the date /time of the new JSON and add the steps of the JSON object and the DB object
            newStepObject = create_or_update_and_get_steps(Steps, stepObject, stepId)
            stepId = stepId + 1
            try:
                newStepObject.save()
            except Exception as e:
                print("couldn't save...")
   
   #old code    
  #      dateMatch = False
  #      stepId = lastStepId + 1
  #      for stepObject in stepsData:
            #find the JSON object that matches that date
  #          dateToCompare = datetime.strptime(stepObject.get('date'),'%Y-%m-%d %H:%M:%S.%f') #2013-11-06
  #          if lastDateStepDate_eastern.date() == dateToCompare.date():
  #              dateMatch = True
  #              stepId = lastDateStepId
            #create an object with the same stepID and patientID
            #add the date /time of the new JSON and add the steps of the JSON object and the DB object
    #        newStepObject = create_or_update_and_get_steps(Steps, stepObject, lastDateStepCount, dateMatch, stepId)
    #        if dateMatch == True:
    #            if stepId == lastStepId:
    #                stepId = stepId + 1
    #            else:
    #                stepId = lastStepId + 1
    #        else:
    #            stepId = stepId + 1
    #        newStepObject.save()
    #        dateMatch = False
    return HttpResponse("True")

def create_or_update_and_get(model_class, data, activityid):
    get_or_create_kwargs = {
        model_class._meta.pk.name: data.pop(model_class._meta.pk.name)
        }
    try:
        # get
        instance = model_class.objects.get(**get_or_create_kwargs)
    except model_class.DoesNotExist:
        # create
        instance = model_class(**get_or_create_kwargs)
    # update (or finish creating)
    for key,value in data.items():
        field = model_class._meta.get_field(key)
        if not field:
            continue
        else:
            if key == 'start_time':
                value = datetime.strptime(value,'%Y-%m-%d %H:%M:%S.%f') #2013-11-06 00:00:00.000
                value_eastern = value.replace()
            setattr(instance, key, value_eastern)
        if isinstance(field, models.ForeignKey) and hasattr(value, 'items'):
            rel_instance = create_or_update_and_get(field.rel.to, value)
            setattr(instance, key, rel_instance)
        else:
            setattr(instance, key, value)
    testPatient = Patient.objects.get(pk=1)
    setattr(instance, 'patientid', testPatient)
    setattr(instance, 'activityid', activityid)
    #instance.save()
    return instance


def create_or_update_and_get_steps(model_class, data, stepId):
    get_or_create_kwargs = {
        model_class._meta.pk.name: data.pop(model_class._meta.pk.name)
        }
    try:
        # get
        instance = model_class.objects.get(**get_or_create_kwargs)
    except model_class.DoesNotExist:
        # create
        instance = model_class(**get_or_create_kwargs)
    # update (or finish creating)
    for key,value in data.items():
        field = model_class._meta.get_field(key)
        if not field:
            continue
        else:
            if key == 'date':
                value = datetime.strptime(value,'%Y-%m-%d %H:%M:%S.%f') #2013-11-06 00:00:00.000
                setattr(instance, 'date', value)
            elif key == 'number_steps':
                setattr(instance, 'number_steps', value)
            #else:
            #    setattr(instance, key, value)
        #if isinstance(field, models.ForeignKey) and hasattr(value, 'items'):
        #    rel_instance = create_or_update_and_get(field.rel.to, value)
        #    setattr(instance, key, rel_instance)
        #else:
        #    setattr(instance, key, value)
    testPatient = Patient.objects.get(pk=1)
    setattr(instance, 'patientid', testPatient)
    setattr(instance, 'stepid', stepId)

    #instance.save()
    return instance


