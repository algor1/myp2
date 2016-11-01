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

def task_new(request):
        if request.method == "POST":
            form = TaskForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.published_date = timezone.now()
                post.save()
                return redirect('tasks.views.task_detail', pk=post.pk)
        else:
            form = TaskForm()
        return render(request,  'tasks/task_new.html', {'form': form})
