from django.db import models

# Create your models here.
class Request(models.Model):
    request_id = models.AutoField(primary_key=True)
    request_display = models.CharField(max_length=100, null=True, blank=True)
    url = models.CharField(max_length=100)
    completed = models.BooleanField(default=False)
    analyze_completed = models.BooleanField(default=False)
