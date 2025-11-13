from rest_framework import serializers
from .models import TaskJob

class TaskJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskJob
        fields = '__all__'
