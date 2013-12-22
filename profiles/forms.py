from __future__ import unicode_literals
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import get_user_model

# from profiles.models import UserProfile


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    error_messages = {
        'duplicate_email': _("A user with that email already exists."),
        'password_mismatch':_("The two password fields didn't match."),
    }
    
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    
    class Meta:
        model = get_user_model()
        fields = ('email', 'first_name', 'last_name')
        
    def clean_password2(self):
        # Checks that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'])
        return password2
    
    def save(self, commit=True):
        # Save the provided password in Hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    
class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's 
    password hash display field.
    Use it to edit User Profiles but hide the password....To 
    implement later sawa.
    """
    
    password = ReadOnlyPasswordHashField()
   
    class Meta:
        model = get_user_model()
        
    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')
        
    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]
    
class PasswordResetRequestForm(forms.Form):
    email = forms.CharField(label=_("Email"))
    
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError(_("No user with that email exists"))
        return email
    
class PasswordResetForm(forms.Form):
    password1 = forms.CharField(label=_("Password"),
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
                                widget=forms.PasswordInput)
    
    def clean_password2(self):
        # Checks that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("The two passwords did not match"))
        return password2
        
class UserProfileEditForm(forms.ModelForm):
    """Users to use this form to edit their profiles
    """
    
    class Meta:
        model = get_user_model()
        
        exclude = ("password", "email", "last_login", "is_superuser", "is_active",
            "is_staff", "is_admin", "date_joined", "groups", "user_permissions")
  
    
