from django.conf.urls import url
from tasks.views import TasksListView,TaskDetailView
from . import views


urlpatterns = [
url(r'^$', TasksListView.as_view(), name='list'), 
url(r'^(?P<pk>\d+)/$', TaskDetailView.as_view(),name='task_detail'), 
url(r'new/$', views.task_new, name='new'), 

]