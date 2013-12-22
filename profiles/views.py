from django.core.urlresolvers import reverse
from django.views import generic
from PIL import Image as PImage
from django.contrib.auth import get_user_model

from profiles.forms import UserCreationForm, UserProfileEditForm

class UserRegistration(generic.CreateView):
    # View for registering the user
    form_class = UserCreationForm
    template_name = 'registration/registration_form.html'
    
    def get_success_url(self):
        return reverse("chapakazi:profile", kwargs={'user.id': self.request.user})
    
class UserProfileDetailView(generic.DetailView):
    # Use has a profile and this is the view
    model = get_user_model()
    slug_field = "email"
    template_name = "user_detail.html"
        
    def get_context_data(self, **kwargs):
        # Implemented a get context data to capture the user objects
        # rather than having a get object which will duplicate the user 
        context = super(UserProfileDetailView, self).get_context_data(**kwargs)
        context['user_list'] = get_user_model().objects.all()
        return context    
    
class UserProfileEditView(generic.UpdateView):
    # Admin view has a user edit but this is for the public
    model = get_user_model()
    form_class = UserProfileEditForm
    template_name = "user_form.html"
    
    def form_valid(self, UserProfileForm):
        """Resize and save profile image."""
        # remove old image if changed
        name = UserProfileForm.cleaned_data.avatar
        pk = self.kwargs.get("mfpk")
        old = get_user_model().objects.get(pk=pk).avatar
        
        if old.name and old.name != name:
            old.delete()
            
        # save new image to disk & resize new image
        self.UserProfileForm_object = UserProfileForm.save()
        if self.UserProfileForm_object.avatar:
            img = PImage.open(self.UserProfileForm_object.avatar.path)
            img.thumbnail((160, 160), PImage.ANTIALIAS)
            img.save(img.filename, "JPEG")
        return reverse(self.success_url)
        
    def get_success_url(self):
        return reverse("chapakazi:profile", kwargs={'slug': self.request.user})
