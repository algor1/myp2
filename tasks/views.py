from django.shortcuts import get_object_or_404,render, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.
from tasks.models import Task, TaskForm, Images, ImagesForm, Comments, CommentsForm
from django.views.generic import ListView, DetailView
from django.utils import timezone

class TasksListView(ListView):
    model = Task              

class TaskDetailView(DetailView):
    model = Task

class ImagesListView(ListView):
    model = Images              


@login_required
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


def detail(request, task_id):

    taskdetail = get_object_or_404(Task, pk=task_id)
    imagesfortask = Images.objects.filter(task=taskdetail)
    commentsfortask=Comments.objects.filter(task=taskdetail)

    if request.method == "POST":
       iform = ImagesForm(request.POST, request.FILES)
       if iform.is_valid():
         formImages = iform.save(commit=False)
         formImages.task=Task.objects.get(pk=task_id)
         formImages.save()
    else:
        
         iform = ImagesForm()
         cform = CommentsForm()

    return render(request, 'tasks/task_detail.html', {'task': taskdetail,'images':imagesfortask, 'comments':commentsfortask, 'iform': iform , 'cform': cform})
	
