from rest_framework import viewsets
from .models import TaskJob
from .serializers import TaskJobSerializer

class TaskJobViewSet(viewsets.ModelViewSet):
    queryset = TaskJob.objects.all()
    serializer_class = TaskJobSerializer
