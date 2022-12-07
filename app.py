from flask import Flask, render_template, request, url_for, redirect, current_app
from pymongo import MongoClient
from datetime import datetime as dtt, date as dt, time as t, timedelta
import time
from collections import defaultdict
import uuid
import os
from dotenv import load_dotenv

#TODO: Ultimate goal is to learn Javascript in order to create a countdown timer in screen and show current progress
#TODO: Option to select if task repeats and the periodicity

load_dotenv()

app = Flask(__name__)

mongo_address = os.getenv("MONGODB_ADDRESS")

client = MongoClient(mongo_address)

app.db = client.flask

def returnToday():
    today = dtt.today()
    return dtt(today.year, today.month, today.day)

possible_hours = [hour for hour in range(1,9)]

# {"_id": uuid, date: selected_date, taskManager: {uuid: {"_id": uuid, "name": taskName,"length": length}}, hoursTaken: [], hoursAvailable: []}}



@app.context_processor
def calc_dateRange():
    def selectDates(startDate: dtt):
        dates_list = [startDate + timedelta(days=diff) for diff in range(-3,4)]
        dates_list.reverse()
        return dates_list
    return {"date_range": selectDates}

def create_task_date_syntax(date: dtt, hours: list):
    return {"date": date, "taskManager": {}, "hoursTaken": [], "hoursAvailable": hours}

@app.route("/")
def home():
    dates_string = request.args.get("date")
    if dates_string:
        selected_date = dtt.fromisoformat(dates_string)
    else:
        selected_date = returnToday()
    todays_day = returnToday()


    current_task_date_object = app.db.taskManager.find_one({"date": selected_date})
    if not current_task_date_object:
        app.db.taskManager.insert_one(create_task_date_syntax(date=selected_date, hours=possible_hours))
        current_task_date_object = app.db.taskManager.find_one({"date": selected_date})
    current_task_manager = current_task_date_object["taskManager"]
    if current_task_manager:
        task_lists = [(task["name"],int(task["length"]), task["_id"]) for task in current_task_manager.values()]
    else:
        task_lists = []

    if selected_date == todays_day:
        tomorrows_date = todays_day + timedelta(days=1)
        preview_task_object = app.db.taskManager.find_one({"date": tomorrows_date})
        if not preview_task_object:
            app.db.taskManager.insert_one(create_task_date_syntax(date=selected_date, hours=possible_hours))
    else:
        preview_task_object = app.db.taskManager.find_one({"date": todays_day})

    if preview_task_object:
        preview_task_manager = preview_task_object["taskManager"]
        preview_tasks = [(task["name"], task["length"]) for task in preview_task_manager.values()]
    else:
        preview_tasks = []


    completions = app.db.completedTasks.find_one({"date": selected_date})
    if completions is None:
        completions = []
    else:
        completions = completions["tasksCompleted"]

    return render_template(
        'home.html', 
        selected_date=selected_date, 
        title="WeeklyPlanner | Home", 
        task_list=task_lists,
        todays_day=todays_day,
        preview=preview_tasks,
        completions=completions
    )


@app.route("/add-task", methods=["GET", "POST"])
def addTask():
    date_string = request.args.get("date")
    if date_string:
        selectedDate = dtt.fromisoformat(date_string)
    else:
        selectedDate = returnToday()
    query_date = {"date": selectedDate}
    date_task_object = app.db.taskManager.find_one(query_date)
    if not date_task_object:
        app.db.taskManager.insert_one(create_task_date_syntax(date=selectedDate, hours=possible_hours))
        date_task_object = app.db.taskManager.find_one(query_date)
    hours_list_available = date_task_object["hoursAvailable"]
    if request.method == "POST" and "date" in request.form:
        response = request.form.get("date")
        date_formated = dtt.fromisoformat(response)
        return redirect(url_for("addTask", date=date_formated))
    if request.method == "POST" and "task" in request.form:
        response = (request.form.get("task"), int(request.form.get("hour")))
        idTask = uuid.uuid4().hex
        new_task = {"_id": idTask ,"name": response[0], "length": response[1]}
        current_task_manager = date_task_object["taskManager"]
        current_task_manager[idTask] = new_task

        current_hours_taken = date_task_object["hoursTaken"]
        current_hours_taken.append(response[1])

        current_hours_available = date_task_object["hoursAvailable"]

        hours_to_remove = []

        for hour_available in current_hours_available:
            if sum(current_hours_taken) + int(hour_available) > 8:
                hours_to_remove.append(hour_available)


        for hour_remove in hours_to_remove:
            current_hours_available.remove(hour_remove)


        updatedValues = {"$set": {"taskManager": current_task_manager, "hoursTaken": current_hours_taken, "hoursAvailable": current_hours_available}}
        app.db.taskManager.update_one(query_date, updatedValues) 

        return redirect(url_for("addTask", date=selectedDate))
    return render_template('add.html', selectedDate=selectedDate, list_hours=hours_list_available)


def complete_task_syntax(date: dtt):
    return {"date": date, "tasksCompleted": []}

@app.route("/complete", methods=["POST"])
def complete():
    task_complete = request.form.get("taskID")
    print(task_complete)
    date_completed = returnToday()
    date_query = {"date": date_completed}
    completed_obj_exists = app.db.completedTasks.find_one(date_query)
    if completed_obj_exists:
        task_list = completed_obj_exists["tasksCompleted"]
        task_list.append(task_complete)
        print(task_list)
        update_obj = {"$set": {"tasksCompleted": task_list}}
        app.db.completedTasks.update_one(date_query, update_obj)
    else:
        app.db.completedTasks.insert_one(complete_task_syntax(date_completed))
        completed_obj_exists = app.db.completedTasks.find_one(date_query)
        print(completed_obj_exists)
        task_list = completed_obj_exists["tasksCompleted"]
        task_list.append(task_complete)
        print(task_list)
        update_obj = {"$set": {"tasksCompleted": task_list}}
        app.db.completedTasks.update_one(date_query, update_obj)
    # {"_id": ... , tasksCompleted: [taskID, taskID]}

    return redirect(url_for("home"))


@app.route("/visualize")
def viewData():
    return render_template('view.html')


if __name__ == "__main__":
    app.run()
