from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

class MyUserManager(BaseUserManager):

    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('email is required')
        if not username:
            raise ValueError('username is required')
        user = self.model(
            email=self.normalize_email(email),
            username=username
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
                   password=password,
                   email=self.normalize_email(email),
                   username=username,
                   )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

def get_profile_image_filepath(self, filename):
    return f'images/{self.date_joined.strftime("%Y")}/{self.date_joined.strftime("%m")}/{self.date_joined.strftime("%d")}/{str(self.pk)}.png'

def get_default_profile_image():
    return "images/statics/No_picture.jpg"

class MyUser(AbstractBaseUser):
    email           = models.EmailField(unique=True, verbose_name='email')
    username        = models.CharField(unique=True, max_length=60)
    firstname       = models.CharField(max_length=60)
    lastname        = models.CharField(max_length=60)
    date_joined     = models.DateTimeField(auto_now_add=True, verbose_name="date joined")
    last_login      = models.DateTimeField(auto_now=True, verbose_name="last login")
    is_admin        = models.BooleanField(default=False)
    is_staff        = models.BooleanField(default=False)
    is_active       = models.BooleanField(default=True)
    is_superuser    = models.BooleanField(default=False)
    profile_image   = models.ImageField(upload_to=get_profile_image_filepath, blank=True, null=True, default=get_default_profile_image)
    
    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    def get_profile_image_filename(self):
        return str(self.profile_image)[str(self.profile_image).index('images/%Y/%m/%d/'):]

    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True
