from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    task_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

class TaskForm(ModelForm):
	class Meta:
		model = Task
		fields = ['task_text', 'pub_date', 'user']
		template_name = 'tasks/task_new.html'