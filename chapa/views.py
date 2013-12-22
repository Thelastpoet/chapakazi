from django.views import generic
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.contrib.auth import get_user_model

from chapa.utils import generic_search
from chapa.models import Task, TaskApplication
from forms import TaskCreateForm, TaskApplicationForm

class IndexView(generic.TemplateView):
    template_name = 'index.html'


class CreateTaskView(generic.CreateView):
    model = Task
    form_class = TaskCreateForm
    template_name = 'task_form.html'
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(CreateTaskView, self).form_valid(form)
         
    def get_context_data(self, **kwargs):
        context = super(CreateTaskView, self).get_context_data(**kwargs)
        context["create_task"] = Task.objects.all()
        return context
    
class TaskEditView(generic.UpdateView):
    model = Task
    form_class = TaskCreateForm
    template_name = 'task_form.html'
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(TaskEditView, self).form_valid(form)
    
        
class TaskListView(generic.ListView):
    model = Task
    template_name = 'task_list.html'
    
    def get_queryset(self):
        return Task.objects.order_by('-pub_date')
    
class TaskDetailView(generic.DeleteView):
    model = Task
    template_name = 'task_detail.html'
    
    
    def get_context_data(self, **kwargs):
        context = super(TaskDetailView, self).get_context_data(**kwargs)
        context["task_list"] = Task.objects.all()
        return context
        
    
class TaskApllicationView(generic.CreateView):
    model = TaskApplication    
    form_class = TaskApplicationForm
    template_name = 'task_applicationform.html'
    
    def form_valid(self, form):
        form.instance.applicant = self.request.user
        
        return super(TaskApllicationView, self).form_valid(form)
    
    def get_success_url(self):
        return reverse("chapakazi:profile", kwargs={'slug': self.request.user})

# Search View begins here

QUERY = "search-query"

MODEL_MAP = {get_user_model(): ["first_name", "last_name", ],
             Task            : ["title", ],
}

def search(request):
    objects = []
    
    for model, fields in MODEL_MAP.iteritems():
        objects += generic_search(request, model, fields, QUERY)
        
    return render_to_response("search_results.html",
                        {"objects":objects,
                         "search_string" : request.GET.get(QUERY, ""),
                         }
                        
    )
# end Search
