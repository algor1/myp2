from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    task_text = models.TextField()
    title = models.CharField(max_length=200, blank=True)
    pub_date = models.DateTimeField('date published')
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

class TaskForm(ModelForm):
	class Meta:
		model = Task
		fields = ['title','task_text']
		template_name = 'tasks/task_new.html'

class Images(models.Model):
    img= models.ImageField(upload_to="users/")
    title = models.CharField(max_length=200, blank=True)
    pub_date = models.DateTimeField('date published')
    
