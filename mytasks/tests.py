import json
from collections import namedtuple
from time import sleep

from django.contrib.auth.models import User, Group
from django.urls import reverse
from rest_framework.test import APITestCase

from dramatiq_tasks_manager.permissions import GROUP_TASK_EXECUTORS


class TasksTestCase(APITestCase):
    def login(self, user):
        """
        Wrapper for self.client.login
        :param user:
        :return:
        """
        return self.client.login(username=user.username,
                                 password=user.password)

    def get(self, path_name, path_kwargs=None, path_app=None):
        """
        Wrapper for self.client.get
        :param path_name:
        :return:
        """
        return self.client.get(reverse(path_name, kwargs=path_kwargs, current_app=path_app))

    def post(self, path_name, data=None, path_kwargs=None, path_app=None):
        """
        Wrapper for self.client.post
        :param path_name:
        :param data:
        :return:
        """
        return self.client.post(reverse(path_name, kwargs=path_kwargs, current_app=path_app),
                                json.dumps(data), content_type='application/json')

    def put(self, path_name, data=None):
        """
        Wrapper for self.client.post
        :param path_name:
        :param data:
        :return:
        """
        return self.client.put(reverse(path_name), json.dumps(data), content_type='application/json')

    def patch(self, path_name, data=None):
        """
        Wrapper for self.client.post
        :param path_name:
        :param data:
        :return:
        """
        return self.client.patch(reverse(path_name), json.dumps(data), content_type='application/json')

    def setUp(self):
        UserDataClass = namedtuple('UserData', ('username', 'email', 'password'))
        self.user_executor_data = UserDataClass(username="3testuser",
                                                email="3test@ema.il",
                                                password="3testpassword")
        self.user_executor = User.objects.create_user(username=self.user_executor_data.username,
                                                      email=self.user_executor_data.email,
                                                      password=self.user_executor_data.password)
        self.group_executor = Group.objects.get(name=GROUP_TASK_EXECUTORS)
        self.user_executor.groups.add(self.group_executor)

    def test_task_find_smallest_in_small_array(self):
        self.assertTrue(self.login(self.user_executor_data))

        print()

        list_data = [3, 9, 14, -3, 2, 7]
        smallest = -3

        payload = {
            'actor_name': 'find_smallest_in_small_array',
            'kwargs': {
                'data': list_data
            }
        }
        post_response = self.post('task_execute', data=payload, path_app='dramatiq_tasks_manager')
        self.assertEqual(201, post_response.status_code,
                         msg=f"Undexpected response_code. Response: {post_response.data}")

        execute_resp_json = post_response.json()
        message_id = execute_resp_json.get('message_id')
        self.assertIsNotNone(message_id, "Message ID is empty. Seems like task wasn't executed")
        sleep(5)
        detail_get_resp = self.get('task_executed_detail',
                                   path_kwargs={'id': message_id},
                                   path_app='dramatiq_tasks_manager')
        self.assertEqual(200, detail_get_resp.status_code,
                         msg=f"Undexpected response_code. Response: {detail_get_resp.data}")
        get_resp_json = detail_get_resp.json()
        self.assertIsNotNone(get_resp_json, "Task data is empty")
        result = get_resp_json.get('result')
        self.assertIsNotNone(result, "Result is empty")
        self.assertEqual(result, smallest)
