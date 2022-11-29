from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient
from datetime import datetime as dtt, date as dt, time as t, timedelta
import time
from collections import defaultdict


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

while appRunning:
    today_date = returnToday()
    hoursToday = sum(dayManager[today_date])
    hoursToRemove = []
    if hoursToday > 0:
        print(hoursToday>0)
        for item in list_hours:
            if item+hoursToday > 8:
                print(item+hoursToday)
                hoursToRemove.append(item)
    for item in hoursToRemove:
        list_hours.remove(item)
    if sum(dayManager[today_date]) < 8:
        assignTask = input(f"Assign a task for Today, {dt.today().strftime('%a, %d')}: ")
        for item in list_hours:
            print(item)
        selectedHour = int(input(f"\nChoose an hour from the above: "))
        taskCounter[assignTask] = selectedHour
        taskManager[today_date] = taskCounter
        dayManager[today_date].append(selectedHour)
    else:
        appRunning = False


# print(f"Finally\n\n\n")

# print(f"You have the following tasks... {[(task, taskTime) for task, taskTime in taskManager[returnToday()].items()]}\n\n\n")

# print(f"For a total of.. {sum(dayManager[returnToday()])}")


test_list = ["Task1", "Task2"]


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

    return render_template('home.html', selected_date=selected_date, title="WeeklyPlanner | Home", test_list=test_list)


    



@app.route("/add-task")
def addTask():
    return render_template('add.html')



@app.route("/visualize")
def viewData():
    return render_template('view.html')