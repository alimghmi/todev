from urllib import response
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse 


class TestTaskAPI(APITestCase):

    def create_not_work_for_anon(self):
        data = {
            "project": 1,
            "title": "A new task",
            "description": "",
            "status": "T",
            "assignees": []
        }
        response = self.client.post(reverse('create-task'), data)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)