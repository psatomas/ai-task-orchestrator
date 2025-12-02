from celery import shared_task
from .models import TaskJob
import time

@shared_task
def execute_task(task_id):
    task = TaskJob.objects.get(id=task_id)

    try:
        task.status = "running"
        task.save()

        # Simulate execution (replace with real logic later)
        time.sleep(2)

        output = {
            "message": f"Task '{task.name}' executed successfully!",
            "input": task.payload,
        }

        task.status = "completed"
        task.result = output
        task.save()

    except Exception as e:
        task.status = "failed"
        task.result = {"error": str(e)}
        task.save()