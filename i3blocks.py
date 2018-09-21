import wunderlist


#task = wunderlist.get_today_tasks()
wunderlist.get_today_tasks()
print("{}".format(task.get('due_date', 'No Tasks Today')))
