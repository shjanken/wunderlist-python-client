import net
from net import WunderClientException
import os
from datetime import date


class WunderlistClient():
    def __init__(self):
        # test the request can be sent
        # 快速失败
        try:
            net.send_request('user')
        except WunderClientException as e:
            print(e)

    def get_list_ids(self):
        """
        return the list of my all wunderlist-list's id
        """
        r = net.send_request('lists')
        return [row.get('id') for row in r.json()]

    def get_list_tasks(self, list_id):
        """
        get list's tasks.
        .e.g: get the study list all tasks
        """
        r = net.send_request('tasks', {'list_id': list_id})
        return r.json()

    def get_today_tasks(self):
        """
        get the tasks due date is today
        """
        today_str = "{:%Y-%m-%d}".format(date.today())

        # get all tasks
        result = [task
                  for id in self.get_list_ids()
                  for task in self.get_list_tasks(id)]

        return [r for r in result if r.get('due_date') == today_str]


if __name__ == '__main__':
    def test_send_request():
        os.environ['X-Access-Token'] = '2673a87e3fb1619117cfb3cabe6810987983218777b7eb672200c1bf2511'
        os.environ['X-Client-ID'] = 'dbe318d9315678615714'

        r = net.send_request('user')
        print(r)
    # test_send_request()

    os.environ['X-Access-Token'] = '2673a87e3fb1619117cfb3cabe6810987983218777b7eb672200c1bf2511'
    os.environ['X-Client-ID'] = 'dbe318d9315678615714'

    c = WunderlistClient()
    print(c.get_today_tasks())
