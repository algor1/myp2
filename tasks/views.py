from django.shortcuts import render

# Create your views here.
from tasks.models import Task, TaskForm 
from django.views.generic import ListView, DetailView

class PostsListView(ListView):
    model = Task              

class PostDetailView(DetailView):
    model = Task

#def task_new(request):
#        form = TaskForm()
#        return render(request, 'tasks/task_new.html', {'form': form})

def task_new(request):
        if request.method == "POST":
            form = TaskForm(request.POST)
            if form.is_valid():
                task = form.save(commit=False)
                task.author = request.user
                task.published_date = timezone.now()
                task.save()
                return redirect('tasks.views.task_detail', pk=task.pk)
        else:
            form = TaskForm()
        return render(request,  'tasks/task_new.html', {'form': form})
