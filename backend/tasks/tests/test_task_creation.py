from unittest.mock import patch
from rest_framework.test import APITestCase
from django.urls import reverse
from tasks.models import TaskJob

class TaskJobTests(APITestCase):
    @patch("tasks.views.execute_task.delay")  # <- mock Celery
    def test_create_taskjob(self, mock_execute):
        url = reverse("taskjob-list")
        data = {"name": "Demo Task", "payload": {"x": 1}}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(TaskJob.objects.count(), 1)
        task = TaskJob.objects.first()
        self.assertEqual(task.status, "pending")

        mock_execute.assert_called_once_with(task.id)