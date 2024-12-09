from django.db import models

# Create your models here.
class rooms(models.Model):
    room_id = models.CharField(max_length=10)
    created_at = models.DateTimeField()
    members = models.IntegerField()
