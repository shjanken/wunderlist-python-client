import unittest
import os
import client
from unittest.mock import patch
from unittest.mock import MagicMock
import requests
from datetime import date


class TestWunderlistClient(unittest.TestCase):
    """
    向 wunderlist 发送请求
    """

    def setUp(self):
        os.environ['X-Access-Token'] = '2673a87e3fb1619117cfb3cabe6810987983218777b7eb672200c1bf2511'
        os.environ['X-Client-ID'] = 'dbe318d9315678615714'

    @patch("net.send_request")
    @patch("requests.Response.json")
    def test_get_list_ids(self, mock_json, mock_send_request):
        """
        test get_list_ids
        mock net.send_request function. do not send request partical
        mock request.Response.json function to mock result
        """
        mock_send_request.return_value = requests.Response()
        mock_json.return_value = [{'id': 232484696}, {'id': 232484736}]

        wl_client = client.WunderlistClient()
        r = wl_client.get_list_ids()
        self.assertEqual(len(r), 2, "the list length should be more than 0")

        # test the failure
        mock_json.return_value = []
        r = wl_client.get_list_ids()
        self.assertEqual(len(r), 0, "should return 0")

    @patch("net.send_request")
    def test_get_list_tasks(self, mock_send_request):
        # mock
        res = requests.Response()
        res.status_code = 200
        res.json = MagicMock(return_value=['test'])
        mock_send_request.return_value = res

        wl_client = client.WunderlistClient()
        tasks = wl_client.get_list_tasks('359935238')
        self.assertGreater(len(tasks), 0,
                           "study list's tasks should more than 0")
        self.assertEqual(tasks, ['test'])

    @patch("net.send_request")
    @patch("client.WunderlistClient.get_list_ids")
    @patch("client.WunderlistClient.get_list_tasks")
    def test_get_today_tasks(self,
                             mock_list_tasks, mock_list_ids,
                             mock_request):
        # mock
        today_str = "{:%Y-%m-%d}".format(date.today())

        # mock net.send_request. not send request particla
        res = requests.Response()
        res.status_code = 200
        mock_request.return_value = res

        mock_list_ids.return_value = ["what ever. just not none"]

        mock_list_tasks.return_value = [{'id':'232484696', 'due_date': '2018-01-01'},
                                        {'id': '23248473', 'due_date': '2019-01-01'},
                                        {'id': '232484740'},
                                        {'id': '232486909',
                                         'due_date':
                                         today_str,
                                         'subject': 'success'}]

        wl_client = client.WunderlistClient()
        tasks = wl_client.get_today_tasks()
        self.assertEqual(len(tasks), 1,
                         "today task should equal or more than 0")
        self.assertEqual("success", tasks[0].get('subject'),
                         "the subject of tasks is 'success'")

    def tearDown(self):
        os.environ.pop('X-Access-Token')
        os.environ.pop('X-Client-ID')


if __name__ == '__main__':
    unittest.main()
