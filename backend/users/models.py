from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """Custom user model extending AbstractUser."""

    def __str__(self):
        return self.username