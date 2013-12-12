from django.http import HttpResponse
from models import Activity
from models import Patient
from models import Steps
from models import Physician
from datetime import datetime, timedelta
import json
#import pprint
import numpy as np
import matplotlib.pyplot as plt
from PyPDF2 import PdfFileWriter, PdfFileReader, PdfFileMerger
import httplib, urllib
import base64
#from io import FileIO as file

def alertFunc():
    phys = Physician.objects.get(physicianid=1)
    pat = Patient.objects.get(patientid=1)
    
    message = '{"RecipientID":'+str(phys.greenway_id)+', "Subject":"Activity Alert", "Body": "Activity for patient has gone outside of threshold. Please go to <a href=https://hit4.nimbus.cip.gatech.edu/getReport>Here</a> to see report!<br /><br />To send report to patient\'s chart, click <a href=https://hit4.nimbus.cip.gatech.edu/sendReport>Here</a> ", "Priority": "High", "PatientID":'+str(pat.greenway_id)+'}'
    headers = {"Content-type": "application/json"}
    conn = httplib.HTTPConnection("hit2.nimbus.cip.gatech.edu")
    conn.request("POST", "/HIESvc/HIE.svc/SendMessage", message, headers)
    resp = conn.getresponse()
    
    return resp.status
    
def sendReport(request): 
    report = file("/group_project/activityappShaneCopy/activityReport.pdf", "r")
    report64 = base64.b64encode(report.read())
    
    phys = Physician.objects.get(physicianid=1)
    pat = Patient.objects.get(patientid=1)
    
    message = '{"DocumentFileType": 4, "PatientID":"'+str(pat.greenway_id)+'", "DocumentName": "ActivityReport.pdf", "Base64Document": "'+str(report64)+'"}'
    headers = {"Content-type": "application/json"}
    conn = httplib.HTTPConnection("hit2.nimbus.cip.gatech.edu")
    conn.request("POST", "/HIESvc/HIE.svc/SendReport", message, headers)
    
    resp = conn.getresponse()
    respData = resp.read()
    return HttpResponse("Sent report! - %s - " % resp.status)

def sendAlert(request): 
    alert = "False"
    if request.method == 'GET':
        
        
        
        return HttpResponse("Sent alert! - %s" % alertFunc())
        
        start = request.GET["start"] if request.GET.__contains__("start") else "2013-11-17"
        end = request.GET["end"] if request.GET.__contains__("end") else  "2013-12-9"
        dateRange = json.dumps([
                           {
                            "start_date" : start,
                            "end_date" : end,
                            }])
        dateRangeData = json.loads(dateRange)
        for dateRangeObj in dateRangeData:

            for key,value in dateRangeObj.items():
                if key == "start_date":
                    startDate = value
                elif key == "end_date":
                    endDate = value
            filteredActivity = [] 
            stepsData = []   
            currentDate = datetime.strptime(startDate,'%Y-%m-%d')
            endDate = datetime.strptime(endDate,'%Y-%m-%d')
            dates = []
            while currentDate <= endDate:
                dayOfActivityData = []
                dates.append(currentDate)
                for actobj in Activity.objects.all():
                    
                    if actobj.start_time.date() == currentDate.date():
                        dayOfActivityData.append(actobj)              
                filteredDayActivity = filterActivityData(dayOfActivityData)
                filteredActivity.append(filteredDayActivity)
                steps = {"steps":0}
                for stepobj in Steps.objects.all():
                    
                    if stepobj.date.date() == currentDate.date():
                        steps = {"steps":stepobj.number_steps}
                stepsData.append(steps)
                currentDate += timedelta(days=1)
                
            alert = makePlot(stepsData, filteredActivity, dates)

    elif request.method == 'POST':
        dateRangeData = json.loads(request.POST['alert'])
        for dateRangeObj in dateRangeData:

            for key,value in dateRangeObj.items():
                if key == "start_date":
                    startDate = value
                elif key == "end_date":
                    endDate = value
            filteredActivity = [] 
            stepsData = []   
            currentDate = datetime.strptime(startDate,'%Y-%m-%d')
            endDate = datetime.strptime(endDate,'%Y-%m-%d')
            dates = []
            while currentDate <= endDate:
                dayOfActivityData = []
                dates.append(currentDate)
                for actobj in Activity.objects.all():
                    
                    if actobj.start_time.date() == currentDate.date():
                        dayOfActivityData.append(actobj)              
                filteredDayActivity = filterActivityData(dayOfActivityData)
                filteredActivity.append(filteredDayActivity)
                steps = {"steps":0}
                for stepobj in Steps.objects.all():
                    
                    if stepobj.date.date() == currentDate.date():
                        steps = {"steps":stepobj.number_steps}
                stepsData.append(steps)
                currentDate += timedelta(days=1)
                
            alert = makePlot(stepsData, filteredActivity, dates)
    
    
    response = HttpResponse("%s" % alert)
    return response

def getReport(request):
    #query database for all activity and steps date range in request
    if request.method == 'GET':
        start = request.GET["start"] if request.GET.__contains__("start") else "2013-11-17"
        end = request.GET["end"] if request.GET.__contains__("end") else  "2013-12-9"
        dateRange = json.dumps([
                           {
                            "start_date" : start,
                            "end_date" : end,
                            }])
        dateRangeData = json.loads(dateRange)
        for dateRangeObj in dateRangeData:

            for key,value in dateRangeObj.items():
                if key == "start_date":
                    startDate = value
                elif key == "end_date":
                    endDate = value
            filteredActivity = [] 
            stepsData = []   
            currentDate = datetime.strptime(startDate,'%Y-%m-%d')
            endDate = datetime.strptime(endDate,'%Y-%m-%d')
            dates = []
            while currentDate <= endDate:
                dayOfActivityData = [] #Activity.objects.filter(start_time__range=[start, end])
                dates.append(currentDate)
                for actobj in Activity.objects.all():
                    
                    if actobj.start_time.date() == currentDate.date():
                        dayOfActivityData.append(actobj)
                
                filteredDayActivity = filterActivityData(dayOfActivityData)
                filteredActivity.append(filteredDayActivity)
                steps = {"steps":0}
                for stepobj in Steps.objects.all():
                    
                    if stepobj.date.date() == currentDate.date():
                        steps = {"steps":stepobj.number_steps}
                stepsData.append(steps)
                currentDate += timedelta(days=1)
                
            alert = makePlot(stepsData, filteredActivity, dates)       
    elif request.method == 'POST':
        dateRangeData = json.loads(request.POST['report'])
        for dateRangeObj in dateRangeData:

            for key,value in dateRangeObj.items():
                if key == "start_date":
                    startDate = value
                elif key == "end_date":
                    endDate = value
            filteredActivity = [] 
            stepsData = []   
            currentDate = datetime.strptime(startDate,'%Y-%m-%d')
            endDate = datetime.strptime(endDate,'%Y-%m-%d')
            while currentDate <= endDate:
                dayOfActivityData = []
                for actobj in Activity.objects.all():
                    
                    if actobj.start_time.date() == currentDate.date():
                        dayOfActivityData.append(actobj)              
                filteredDayActivity = filterActivityData(dayOfActivityData)
                filteredActivity.append(filteredDayActivity)
                steps = {"steps":0}
                for stepobj in Steps.objects.all():
                    
                    if stepobj.date.date() == currentDate.date():
                        steps = {"steps":stepobj.number_steps}
                stepsData.append(steps)
                currentDate += timedelta(days=1)
                
            alert = makePlot(stepsData, filteredActivity, dateRangeData)
    
    
    
    output = open("/group_project/activityappShaneCopy/activityReport.pdf", "rb")
    response = HttpResponse(output, content_type='application/pdf')
    response['Content-Disposition'] = 'filename="activityReport.pdf"'
    
	#output.readall()
    #response.write(output) 
    return response
    #return HttpResponse("report created! - %s, %s" %(stepsData, filteredActivity))


def filterActivityData(dayOfActivityData):
    #filter
    walkingArray = []
    runningArray = []
    stationaryArray = []
    carArray = []
    unknownArray = []
    lastobj = Activity(duration=0,type=1)
    sumDuration = 0
    for actobj in dayOfActivityData:
        if actobj.type == 1:
            if lastobj.type == 1:
                if len(walkingArray) > 0:
                    sumDuration = actobj.duration + walkingArray[len(walkingArray)-1]
            else:
                sumDuration = actobj.duration
            walkingArray.append(sumDuration)
        elif actobj.type == 2:
            if lastobj.type == 2:
                if len(runningArray) > 0:
                    sumDuration = actobj.duration + runningArray[len(runningArray)-1]
            else:
                sumDuration = actobj.duration
            runningArray.append(sumDuration)
        elif actobj.type == 3:
            if lastobj.type == 3:
                if len(stationaryArray) > 0:
                    sumDuration = actobj.duration + stationaryArray[len(stationaryArray)-1]
            else:
                sumDuration = actobj.duration
            stationaryArray.append(sumDuration)
        elif actobj.type == 4:
            if lastobj.type == 4:
                if len(carArray) > 0:
                    sumDuration = actobj.duration + carArray[len(carArray)-1]
            else:
                sumDuration = actobj.duration
            carArray.append(sumDuration)
        else:    
            if lastobj.type == 5:
                if len(unknownArray) > 0:
                    sumDuration = actobj.duration + unknownArray[len(unknownArray)-1]
            else:
                sumDuration = actobj.duration
            unknownArray.append(sumDuration)
            lastobj = actobj
            lastobj.duration = actobj.duration
            lastobj.type = actobj.type
    filteredData = {"walking":walkingArray,"running":runningArray,"stationary":stationaryArray,"car":carArray,"unknown":unknownArray}
    return filteredData

def makePlot(stepData, filteredActivity, dateRangeData):
    tupleOfDates  = dateRangeData
    tupleOfDays = []
    tupleOfLabels = []
    tupleOfWeeks = []
    for index in range(len(tupleOfDates)):
        currentDate = tupleOfDates[index]
        currentDay = currentDate.strftime("%A")
        currentMonth = currentDate.month
        currentDayNum = currentDate.day
        startOfWeek = currentDate - timedelta(days=6)
        startOfWeekMonth = startOfWeek.month
        startOfWeekDayNum = startOfWeek.day
        #if (index == 0 | (len(tupleOfDates)-1)):
        if (index >= 0):
            
            labelText = "%s/%s" %(currentMonth,currentDayNum) 
            text = "%s" %currentDay
            if (currentDay == "Saturday"):
                labelText = labelText = "Sat - %s/%s" %(currentMonth,currentDayNum)
            if (currentDay== "Sunday"):
                labelText = labelText = "Sun - %s/%s" %(currentMonth,currentDayNum)
            tupleOfDays.append(text)
            tupleOfLabels.append(labelText)
        else:
            tupleOfDays.append(currentDay)

        text = "%s/%s - %s/%s" %(startOfWeekMonth,startOfWeekDayNum,currentMonth,currentDayNum)
        tupleOfWeeks.append(text)
            
    for index in range(len(tupleOfLabels)):
        if ((index != 0) & (index != (len(tupleOfLabels)-1))):
            if ((tupleOfDays[index] == "Saturday") & (tupleOfDays[index] == "Sunday")):
                tupleOfDays[index] = ""
            
    for index in range(len(tupleOfWeeks)):
        if (index != (len(tupleOfWeeks)-1)):
            if (index%2 == 1):
                tupleOfWeeks[index] = ""
    
    dictOfThresholds = {'low active': 5000, 'somewhat active': 7500, 'active': 10000, 'highly active': 12500}
    
    patient = Patient.objects.get(patientid=1)
    
    patientName = patient.first_name+", "+patient.last_name
    recordNumber = patient.greenway_id
    
    
    # Stores activity thresholds (i.e., moderate, highly active, etc.)
    listOfThresholdKeys = list(dictOfThresholds.keys())
    listOfThresholdValues = list(dictOfThresholds.values())
    
    # Makes a tuple of daily step values
    tupleOfStepValues = ([])
    for x in stepData:
        tupleOfStepValues.append(x['steps'])
    
    # The x-axis
    indSteps = np.arange(len(stepData))
    width = 0.35       # the width of the bars: can also be len(x) sequence
    
    # Make plot number 1
    fig, ax = plt.subplots()
    ax.plot(indSteps, tupleOfStepValues, 'o-')
    for index in range(len(tupleOfStepValues)):
        xValue = indSteps[index]
        if (tupleOfDays[index] == "Saturday"):
            xValue = xValue - width/2
            ax.plot([xValue,xValue],[0,15000],'k-',lw=3)
        if (tupleOfDays[index] == "Sunday"):
            xValue = xValue + width/2
            ax.plot([xValue,xValue],[0,15000],'k-',lw=3)
    plt.ylabel('Steps')
    graphTitleSteps = patientName + ' - ' + recordNumber + ' - Daily Steps Count'
    plt.title(graphTitleSteps)
    plt.xticks(indSteps, tupleOfLabels )
    fig.autofmt_xdate()
    plt.ylim(0,max(listOfThresholdValues )+2500)
    a = plt.axhspan(0, 5000, facecolor='red', alpha=0.6)
    a = plt.axhspan(5000, 7500, facecolor='red', alpha=0.3)
    a = plt.axhspan(7500, 10000, facecolor='green', alpha=0.3)
    a = plt.axhspan(10000, 12500, facecolor='green', alpha=0.6)
    a = plt.axhspan(12500, 15000, facecolor='green', alpha=0.9)
    # Add the thresholds into the plot
    for x in np.arange(len(listOfThresholdValues)):
        plt.text(0.1,listOfThresholdValues[x-1],listOfThresholdKeys[x-1], va='bottom')
        ax.plot([0,len(stepData)],[listOfThresholdValues[x-1], listOfThresholdValues[x-1]], 'g--')
        
    
        
    
    # Save files and show figure
    plt.savefig('/group_project/activityappShaneCopy/activitySteps.png')
    plt.savefig('/group_project/activityappShaneCopy/activitySteps.pdf')
    
    #plt.show()
    
    # Initiation of activity duration counters
    walking_counter = []
    running_counter = []
    stationary_counter = []
    driving_counter = []
    #unknown_counter = []
        
    # Add up all the seconds of activity for each day and store them in a list
    for x in np.arange(len(filteredActivity)):
        walking_counter.append(sum(list(filteredActivity[x].get('walking'))))
        running_counter.append(sum(list(filteredActivity[x].get('running'))))
        driving_counter.append(sum(list(filteredActivity[x].get('car'))))
        stationary_counter.append(sum(list(filteredActivity[x].get('stationary'))))
    
    # Convert from seconds to minutes and round the values
    for x in np.arange(len(filteredActivity)):
        walking_counter[x] = int(round(walking_counter[x]/60))
        running_counter[x] = int(round(running_counter[x]/60))
        driving_counter[x] = int(round(driving_counter[x]/60))
        stationary_counter[x] = int(round(stationary_counter[x]/60))
    
    # Initiation and conversion for plot number 2
    walking_counter = np.array(walking_counter)
    listOfSteps = np.arange(len(walking_counter))
    listOfZeros = np.zeros(len(walking_counter))
    ticks = np.arange(24)
    minutesTicks = []
    hoursTicks = []
    for index in range(len(ticks)):
        minutes = (index+1)*60
        hours = (index+1)
        minutesTicks.append(minutes)
        hoursTicks.append(hours)
        
    
    #create stacks
    stationaryStack_counter = []
    walkingStack_counter = []
    for index in range(len(running_counter)):
        value = running_counter[index]+walking_counter[index]
        walkingStack_counter.append(value)
        value = value + stationary_counter[index]
        stationaryStack_counter.append(value)
    
        
    
    # Make plot number 2
    fig2, (ax2) = plt.subplots(1,1)
    for index in range(len(tupleOfStepValues)):
        xValue = indSteps[index]
        if (tupleOfDays[index] == "Saturday"):
            xValue = xValue - width/2
            ax2.plot([xValue,xValue],[0,1440],'k-',lw=3)
        if (tupleOfDays[index] == "Sunday"):
            xValue = xValue + width/2
            ax2.plot([xValue,xValue],[0,1440],'k-',lw=3)
    ax2.fill_between(listOfSteps, running_counter, walkingStack_counter, facecolor = 'red', alpha=0.3)
    ax2.fill_between(listOfSteps, listOfZeros, running_counter, facecolor = 'green', alpha=0.3)
    ax2.fill_between(listOfSteps, walkingStack_counter, stationaryStack_counter, facecolor = 'blue', alpha=0.3)
    ax2.fill_between(listOfSteps, stationaryStack_counter, 1440, facecolor = 'black', alpha=0.3)
    plt.ylim(0,1440)
    plt.ylabel('Duration (hr)')
    plt.yticks(minutesTicks,hoursTicks)
    graphTitleDuration = patientName + ' - ' + recordNumber + ' - Daily Duration of Activity'
    plt.title(graphTitleDuration)
    plt.xticks(listOfSteps, tupleOfLabels)
    fig2.autofmt_xdate()
    labels = ['walking', 'running', 'stationary', 'other']
    p1 = plt.Rectangle((0,0), 1, 1, fc="red", alpha=0.3)
    p2 = plt.Rectangle((0,0), 1, 1, fc="green", alpha=0.3)
    p3 = plt.Rectangle((0,0), 1, 1, fc="blue", alpha=0.3)
    p4 = plt.Rectangle((0,0), 1, 1, fc="black", alpha=0.3)
    plt.legend([p1, p2, p3, p4], labels)
    
    plt.savefig('/group_project/activityappShaneCopy/activityDuration.png')
    plt.savefig('/group_project/activityappShaneCopy/activityDuration.pdf')
    
    #plt.show()
    
    # Calculate running average for step data
    daysForRunningAverage = 7; #works best for odd numbers
    tupleOfRunningAveragesSteps = ([])
    
    for i in np.arange(len(tupleOfStepValues)):
        iterationStart = int(i - ((daysForRunningAverage-1)/2))
        if iterationStart < 1:
            iterationStart = 1
        iterationEnd = int(i + ((daysForRunningAverage-1)/2))
        if iterationEnd > len(tupleOfStepValues):
            iterationEnd = len(tupleOfStepValues)
        runningSum = 0
        for j in range(iterationStart, iterationEnd + 1):
            runningSum = runningSum + tupleOfStepValues[j-1]
        runningSum = runningSum / (iterationEnd - iterationStart + 1)
        tupleOfRunningAveragesSteps.append(runningSum)
        
    # Make plot 3 (Running averages of steps)
    fig3, ax3 = plt.subplots()
    for index in range(len(tupleOfRunningAveragesSteps)):
        xValue = indSteps[index]
        ax3.plot([xValue,xValue],[0,15000],'k-',lw=0.5,color='0.5')
    ax3.plot(indSteps, tupleOfRunningAveragesSteps, 'o-')

    graphYLabel = 'Steps (' + str(daysForRunningAverage) + '-day Rolling Average)'
    plt.ylabel(graphYLabel)
    graphTitleStepsRunningAverage = patientName + ' - ' + recordNumber + ' - Daily Steps Count (Rolling Average)'
    plt.title(graphTitleStepsRunningAverage)
    plt.xticks(indSteps, tupleOfWeeks )
    fig3.autofmt_xdate()
    plt.ylim(0,max(listOfThresholdValues )+2500)
    a = plt.axhspan(0, 5000, facecolor='red', alpha=0.6)
    a = plt.axhspan(5000, 7500, facecolor='red', alpha=0.3)
    a = plt.axhspan(7500, 10000, facecolor='green', alpha=0.3)
    a = plt.axhspan(10000, 12500, facecolor='green', alpha=0.6)
    a = plt.axhspan(12500, 15000, facecolor='green', alpha=0.9)
    # Add the thresholds into the plot
    for x in np.arange(len(listOfThresholdValues)):
        plt.text(0.1,listOfThresholdValues[x-1],listOfThresholdKeys[x-1], va='bottom')
        ax3.plot([0,len(stepData)],[listOfThresholdValues[x-1], listOfThresholdValues[x-1]], 'g--')
        
    # Save files and show figure
    plt.savefig('/group_project/activityappShaneCopy/activityStepsRunningAverage.png')
    plt.savefig('/group_project/activityappShaneCopy/activityStepsRunningAverage.pdf')
    
    #plt.show()
    
    # Merge the three .pdf files into a single file (had to install PyPDF package and add a line of code to make it compatible with Python 3.3
    #merger = PdfFileMerger()
     
    output = PdfFileWriter()
    pg1 = PdfFileReader(file("/group_project/activityappShaneCopy/activityDuration.pdf", "rb"))
    pg2 = PdfFileReader(file("/group_project/activityappShaneCopy/activitySteps.pdf", "rb"))
    pg3 = PdfFileReader(file("/group_project/activityappShaneCopy/activityStepsRunningAverage.pdf", "rb"))
	
    output.addPage(pg3.getPage(0))
    output.addPage(pg2.getPage(0))
    output.addPage(pg1.getPage(0))
	
    #input2 = open("/group_project/activityappShaneCopy/activitySteps.pdf", "rb")
    #input3 = open("/group_project/activityappShaneCopy/activityDuration.pdf", "rb")
    #input1 = open("/group_project/activityappShaneCopy/activityStepsRunningAverage.pdf", "rb")
    
    #merger.append(input1)
    #merger.append(input2)
    #merger.append(input3)
    
    outFile = file("/group_project/activityappShaneCopy/activityReport.pdf", "wb")
    output.write(outFile)
    outFile.close()
    
    #business logic
    #if rolling average for is at one level for at least 7 data points and then goes down a level for that many data points &
    responseTest = False
    ratingList = []
    for obj  in tupleOfRunningAveragesSteps:
        if (obj > 12500):
            ratingList.append(4)
        elif (obj > 10000):
            ratingList.append(3)
        elif (obj > 7500):
            ratingList.append(2)
        elif (obj > 5000):
            ratingList.append(1)
        else:
            ratingList.append(0)
            
    trendLine1 = 0
    trendLine2 = 0
    currentTrend1Rating = 5
    responseTest = False
    
    for index in range(len(ratingList)):
        if (trendLine1 < 7):
            if (ratingList[index] == currentTrend1Rating):
                trendLine1 = trendLine1 + 1
            else:
                currentTrend1Rating = ratingList[index]
        else:
            if (index > 13):
                indexMin = index - 13
                indexMax = index - 7
                
                for index2 in range(indexMin,indexMax):
                    if (ratingList[index2] > currentTrend1Rating):
                        trendLine2 = trendLine2 + 1
                    else:
                        trendLine2 = 0

            if (trendLine2 >= 7):
                responseTest = True
    response = "%s" % responseTest
    
    return response