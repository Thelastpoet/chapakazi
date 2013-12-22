from django.conf.urls import patterns, url

from chapa import views

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(template_name="index.html"), name='index'),
    url(r'^taskcreate/$', views.CreateTaskView.as_view(), name="create-task"),
    url(r'^tasklist/$', views.TaskListView.as_view(), name="task-list"),
    url(r'^taskedit/(?P<pk>\d+)/$', views.TaskEditView.as_view(), name="task-edit"),
    url(r'taskdetail/(?P<pk>\d+)/$', views.TaskDetailView.as_view(), name="task-detail"),
    
    url(r'^taskapply/$', views.TaskApllicationView.as_view(), name="apply-task"),
    url(r'^search/$', views.search, name="search"),
    
)
