from rest_framework.test import APIClient
from django.urls import reverse
from tasks.models import TaskJob
import pytest

@pytest.mark.django_db
def test_taskjob_start_endpoint():
    client = APIClient()

    # Create a TaskJob
    task = TaskJob.objects.create(
        name="Sample Task",
        description="Test description"
    )

    url = reverse("taskjob-start", args=[task.id])
    response = client.post(url)

    assert response.status_code == 200
    task.refresh_from_db()

    assert task.started_at is not None
    assert task.completed is False