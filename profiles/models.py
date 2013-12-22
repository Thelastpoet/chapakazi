from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

GENDER = (
    ('M', 'Male'),
    ('F', 'Female'),
)

SKILLS = (
    ('I', 'I'),
    ('W', 'Web Development'),
)

from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin,
)

class Location(models.Model):
    county = models.CharField(max_length=255)
    town = models.CharField(max_length=255)
    constituency = models.CharField(max_length=255)
    area_code = models.CharField(max_length=255)
    
    def __unicode__(self):
        return self.town

class WebUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('Users must have an email address')
        
        user = self.model(
            email=WebUserManager.normalize_email(email),
            is_staff=False, is_active=True, is_superuser=False,
            last_login=now, date_joined=now, **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
            
    def create_superuser(self, email, password, **extra_fields):
        """
        Creates and saves a superuser with the given email, and password.
        """
        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user
    
class WebUser(AbstractBaseUser, PermissionsMixin):
    
    objects = WebUserManager()
    
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        db_index=True,
    )
    first_name = models.CharField(max_length=255,
            db_index=True)
    last_name = models.CharField(max_length=255,
            db_index=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER)
    address = models.CharField(max_length=255),
    postal_code = models.CharField(max_length=255)
    city = models.ForeignKey(Location, blank=True, null=True)
    country = models.CharField(max_length=255)
   
    avatar = models.ImageField("Profile Pic", upload_to="images/", blank=True, null=True)
    skills = models.CharField(max_length=1, choices=SKILLS)
    other_skills = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)  # Needs to be changed
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now())
    # Add later user categories
    # like those who can register as employers or freelancers
    
    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['email']
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        
    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.username)
    
    def get_full_name(self):
        # The user is identified by their full names.
        # returns first name and the last name with a space between the two
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()
    
    def get_short_name(self):
        # The user should be identified by their last name or surname
        return self.first_name
    
    def email_user(self, subject, message, from_email=None):
        # Sends an email to this user
        send_mail(subject, message, from_email, [self.email])
    
    def __unicode__(self):
        return "%s' profile" % self.first_name
        
    def has_perm(self, perm, obj=None):
        # Users who are employers should have permissions to create tasks
        # Research on how to implement this
        return True  # for now 
    
    def avatar_image(self):
        return (settings.MEDIA_URL + self.avatar.name) if self.avatar else None

class PasswordReset(models.Model):
    user = models.ForeignKey(WebUser)
    key = models.CharField(max_length=100)
    used = models.BooleanField(default=False)

