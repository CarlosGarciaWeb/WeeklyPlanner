from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient
from datetime import datetime as dtt, date as dt, time as t
import time
from collections import defaultdict


print(dtt.today(), dt.today, f"\n\n")

app = Flask(__name__)

list_hours = [hour for hour in range(1,9)]


def returnToday():
    today = dtt.today()
    return dtt(today.year, today.month, today.day)

taskCounter = defaultdict(t)

taskManager = defaultdict(dict)

dayManager = defaultdict(list)

appRunning = True

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


print(f"Finally\n\n\n")

print(f"You have the following tasks... {[(task, taskTime) for task, taskTime in taskManager[returnToday()].items()]}\n\n\n")

print(f"For a total of.. {sum(dayManager[returnToday()])}")


    
