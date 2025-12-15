from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from .models import TaskJob
from .serializers import TaskJobSerializer
from .tasks import execute_task


class TaskJobViewSet(viewsets.ModelViewSet):
    queryset = TaskJob.objects.all()
    serializer_class = TaskJobSerializer

    def perform_create(self, serializer):
        task = serializer.save(status="pending")
        execute_task.delay(task.id)

    @action(detail=True, methods=["post"])
    def retry(self, request, pk=None):
        task = self.get_object()

        if task.status == "running":
            return Response(
                {"error": "Task is already running"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        task.status = "pending"
        task.result = None
        task.save(update_fields=["status", "result"])

        execute_task.delay(task.id)

        return Response(
            {"status": f"Task {task.id} retried"},
            status=status.HTTP_200_OK,
        )

