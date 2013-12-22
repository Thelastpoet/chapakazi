from django import forms
from django.db import models
from chapa.models import Task, TaskApplication

class TaskCreateForm(forms.ModelForm):
    
    class Meta:
        model = Task
        exclude = ('owner',)
        
class TaskApplicationForm(forms.ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'
    formfield_overides = {models.TextField: {'widget': forms.Textarea(attrs=
            {'class':'ckeditor'})}, }  
      
    class Meta:
        model = TaskApplication
        exclude = ["applicant", ]
        
        def __init__(self, *args, **kwargs):
            super(TaskApplicationForm, self).__init__(*args, **kwargs)
            self.fields['task'].initial = self.request.task
        
    class Media:
        js = ('ckeditor.js',)
        
    def clean_applicant(self):
        return self.cleaned_data.get("applicant")
    
