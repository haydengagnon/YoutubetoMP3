from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class MP3File(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file_path = models.CharField(max_length=255)
    title = models.CharField(max_length=100)
    posted = models.BooleanField(default=False)
    file_size = models.FloatField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)