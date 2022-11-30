from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient
from datetime import datetime as dtt, date as dt, time as t, timedelta
import time
from collections import defaultdict
import uuid

#TODO: Ultimate goal is to learn Javascript in order to create a countdown timer in screen and show current progress
#TODO: Render form and dates to organize planner


print(dtt.today(), dt.today, f"\n\n")

app = Flask(__name__)

list_hours = [hour for hour in range(1,9)]


def returnToday():
    today = dtt.today()
    return dtt(today.year, today.month, today.day)

taskCounter = defaultdict(t)

taskManager = defaultdict(dict)

dayManager = defaultdict(list)

appRunning = False

# while appRunning:
#     today_date = returnToday()
#     hoursToday = sum(dayManager[today_date])
#     hoursToRemove = []
#     if hoursToday > 0:
#         print(hoursToday>0)
#         for item in list_hours:
#             if item+hoursToday > 8:
#                 print(item+hoursToday)
#                 hoursToRemove.append(item)
#     for item in hoursToRemove:
#         list_hours.remove(item)
#     if hoursToday < 8:
#         assignTask = input(f"Assign a task for Today, {dt.today().strftime('%a, %d')}: ")
#         for item in list_hours:
#             print(item)
#         selectedHour = int(input(f"\nChoose an hour from the above: "))
#         taskCounter[assignTask] = selectedHour
#         taskManager[today_date] = taskCounter
#         dayManager[today_date].append(selectedHour)
#     else:
#         appRunning = False

def calculatePossibleHours(date: dtt):
    global dayManager, list_hours
    hoursToRemove = []
    hoursToday = sum(dayManager[date])
    if hoursToday > 0:
        for hour in list_hours:
            if hour+hoursToday > 8:
                hoursToRemove.append(hour)
    for hourR in hoursToRemove:
        list_hours.remove(hourR)
    return hoursToday

# {dateId: [1, 2, 3, 5]}

# {task: [1, False]}

# {"_id": id, date: {task:1,task2:2}}




test_list = []


@app.context_processor
def calc_dateRange():
    def selectDates(startDate: dtt):
        dates_list = [startDate + timedelta(days=diff) for diff in range(-3,4)]
        dates_list.reverse()
        return dates_list
    return {"date_range": selectDates}



@app.route("/")
def home():
    dates_string = request.args.get("date")
    if dates_string:
        selected_date = dtt.fromisoformat(dates_string)
    else:
        selected_date = returnToday()
    todays_day = returnToday()
    hoursAvailable = calculatePossibleHours()
    return render_template(
        'home.html', 
        selected_date=selected_date, 
        title="WeeklyPlanner | Home", 
        test_list=test_list,
        todays_day=todays_day,
        hoursAvailable=hoursAvailable
    )


    



@app.route("/add-task", methods=["GET", "POST"])
def addTask():
    global taskCounter, taskManager, dayManager
    date_string = request.args.get("date")
    hoursAvailable = request.args.get("hours")
    if date_string:
        selectedDate = dtt.fromisoformat(date_string)
    else:
        selectedDate = returnToday()
    if request.method == "POST" and "date" in request.form:
        response = request.form.get("date")
        date_formated = dtt.fromisoformat(response)
        return redirect(url_for("addTask", date=date_formated, list_hours=list_hours))
    if hoursAvailable < 8:
        if request.method == "POST" and "task" in request.form:
            response = (request.form.get("task"), request.form.get("hour"))
            taskCounter[response[0]] = response[1]
            taskManager[selectedDate] = taskCounter
            dayManager[selectedDate].append(response[1])
            hoursAvailable = calculatePossibleHours()
            return redirect(url_for("addTask", selectedDate=selectedDate, list_hours=list_hours))
    return render_template('add.html', selectedDate=selectedDate, list_hours=list_hours)



@app.route("/visualize")
def viewData():
    return render_template('view.html')