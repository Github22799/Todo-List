from django.db import models


class Todo(models.Model):
    title = models.CharField(max_length=200)
    memo = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_completed = models.DateTimeField()
    important = models.BooleanField(default=False)
