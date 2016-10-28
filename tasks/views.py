from django.shortcuts import render

# Create your views here.
from tasks.models import Task, TaskForm 
from django.views.generic import ListView, DetailView

class PostsListView(ListView):
    model = Task              

class PostDetailView(DetailView):
    model = Task

def task_new(request):
        form = TaskForm()
        return render(request, 'tasks/task_new.html', {'form': form})

