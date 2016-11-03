from django.shortcuts import render, redirect

# Create your views here.
from tasks.models import Task, TaskForm 
from django.views.generic import ListView, DetailView
from django.utils import timezone

class TasksListView(ListView):
    model = Task              

class TaskDetailView(DetailView):
    model = Task


def task_new(request):
        if request.method == "POST":
            form = TaskForm(request.POST)
            if form.is_valid():
                Task = form.save(commit=False)
                Task.user = request.user
                Task.pub_date = timezone.now()

                if not Task.title:
                	Task.title=Task.task_text[:50]
		
                Task.save()
                return redirect('list')
        else:
            form = TaskForm()
        return render(request,  'tasks/task_new.html', {'form': form})

