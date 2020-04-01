from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# from django.core.urlresolvers import reverse

# Create your models here.
class Task(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=200)
    super_task = models.ForeignKey('self', on_delete=models.CASCADE, null = True, blank = True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null = True, blank = True, related_name='tasks')

    def  get_absolute_url(self):
        return reverse("task:index")
    
    def __str__(self):
        return self.name+" "+str(self.super_task)
    