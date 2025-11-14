from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Task
from .serializers import TaskJobSerializer
from django.utils import timezone

class TaskJobViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskJobSerializer

    @action(detail=True, methods=['post'])
    def start(self, request, pk=None):
        task = self.get_object()
        if getattr(task, "started_at", None):
            return Response({"status": f"Task {task.id} already started"}, status=400)
        
        # Example logic: mark task as started
        task.started_at = timezone.now()
        task.completed = False
        task.save()
        return Response({"status": f"Task {task.id} started"})

