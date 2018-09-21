import requests
from datetime import date


class WunderlineClient:

    def __init__(self):
        self.auth_para = {
            'X-Access-Token': '2673a87e3fb1619117cfb3cabe6810987983218777b7eb672200c1bf2511',
            'X-Client-ID': 'dbe318d9315678615714'
        }

        self.comm_url = 'http://a.wunderlist.com/api/v1/{res}'
        self.user_url = self.comm_url.format(res='user')
        self.lists_url = self.comm_url.format(res='lists')

    def send_request_with_auth_params(self, url):
        return requests.get(url, headers=self.auth_para)

    def get_user_info(self):
        r = self.send_request_with_auth_params(self.user_url)
        result = r.json()
        print(result['name'])

    def get_lists(self):
        r = self.send_request_with_auth_params(self.lists_url)
        list_ids = []
        for result in r.json():
            list_ids.append(result['id'])
        return list_ids

    def get_list_tasks(self, list_id):
        r = requests.get('https://a.wunderlist.com/api/v1/tasks',
                         params={'list_id': olist_id},
                         headers=self.auth_para)
        return r.json()

    def get_today_tasks(self):
        # get date
        today_str = "{:%Y-%m-%d}".format(date.today())
        # get tasks
        list_ids = self.get_lists()  # get my all list ids
        all_tasks = [task
                     for id in list_ids
                     for task in self.get_list_tasks(id)]

        # filter tasks if tasks's due_time is not none
        has_due_time_tasks = [task
                              for task in all_tasks
                              if task.get('due_date') is not None]
        # the due_time is today?
        # return
        return [task
                for task
                in has_due_time_tasks if task.get('due_date') == today_str]


# list_ids = get_lists()
# list = [task for tasks in tmp for task in tasks]
# print(list)
