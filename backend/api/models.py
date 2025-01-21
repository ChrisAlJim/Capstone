from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Idea(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    thinker = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ideas")

    def __str__(self):
        return self.title