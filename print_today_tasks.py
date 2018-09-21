from wunderlist.client import WunderlistClient

client = WunderlistClient()

tasks = client.get_today_tasks()
for task in tasks:
    print("{}\n".format(task.get('title')))
