from ckeditor.fields import RichTextField
from tinymce.models import HTMLField
from django.db import models
from django.contrib.auth import get_user_model
        
    
class Task(models.Model):
    title = models.CharField(max_length=255)
    pub_date = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(get_user_model())
    task_category = models.CharField(max_length=255)  # like IT, marketing
    skills_requird = models.CharField(max_length=255)  # Skills users need to have  
    description = HTMLField()
    due_date = models.DateTimeField()
    task_type = models.CharField(max_length=255)  # how you will pay the freelencer
    budget = models.CharField(max_length=255)  # How much you intent to pay the Freelencer
    
    
    class Meta:
        ordering = ["pub_date"]
        
    def __unicode__(self):
        return self.title
    
    def short(self):
        pub_date = self.pub_date.strftime("%b %d, %I:%M %p")
        return u"%s - %s\n%s" % (self.pub_date, self.title, pub_date)
    
    def profile_data(self):
        p = self.owner.profile
        return p.tasks, p.avatar
    
    def get_absolute_url(self):
        return "chapa:task-detail/%s/" % self.title
    
class TaskApplication(models.Model):
    applicant = models.ForeignKey(get_user_model())
    task = models.ForeignKey(Task)
    application_date = models.DateTimeField(auto_now_add=True)
    app_form = models.TextField()
    
    def __unicode__(self):
        return u"s: %s" % (self.task, self.app_form[:50])
    """
    def save(self, *args, **kwargs):
        #Email owner when someone applies.
        if notify:
            tpl = "An Application was made on '%s' by '%s': \n\n%s"
            message = tpl % (self.task, self.applicant, self.app_form)
            from_addr = "no-reply@mydomain.com"
            recipient_list = ["myemail@mydomain.com"]
            
            send_mail("An Application is Made", message, from_addr, recipient_list)
        super(TaskAplication, self).save(*args, **kwargs)
    """
