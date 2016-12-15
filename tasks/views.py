from django.shortcuts import get_object_or_404,render, redirect

# Create your views here.
from tasks.models import Task, TaskForm, Images, ImagesForm
from django.views.generic import ListView, DetailView
from django.utils import timezone

class TasksListView(ListView):
    model = Task              

class TaskDetailView(DetailView):
    model = Task

class ImagesListView(ListView):
    model = Images              

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

def image_new(request, task_id):
        if request.method == "POST":
            form = ImagesForm(request.POST, request.FILES)
            if form.is_valid():
                Images = form.save(commit=False)
                Images.task=Task.objects.get(pk=task_id)
##                Images.image=request.FILES['image']
                Images.save()
                return redirect('list')
        else:
            form = ImagesForm()
        return render(request,  'tasks/image_new.html', {'form': form})



def detail(request, task_id):
    taskdetail = get_object_or_404(Task, pk=task_id)
    imagesfortask =Images.objects.filter(task=taskdetail)
    return render(request, 'tasks/task_detail.html', {'task': taskdetail,'images':imagesfortask})
