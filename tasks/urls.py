from django.conf.urls import url
from tasks.views import TasksListView,TaskDetailView,ImagesListView
from . import views


urlpatterns = [
url(r'^$', TasksListView.as_view(), name='list'), 
url(r'^(?P<pk>\d+)/$', TaskDetailView.as_view(),name='task_detail'),
url(r'^(?P<pk>\d+)/images/$', ImagesListView.as_view(),name='task_images'),
url(r'new/$', views.task_new, name='new'),
url(r'image_new/$', views.image_new, name='image_new'),
url(r'^(?P<task_id>\d+)/d/$', views.detail ,name='detail'),


]
