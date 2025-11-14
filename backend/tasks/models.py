from django.db import models

class TaskJob(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    started_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

