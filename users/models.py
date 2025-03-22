from django.db import models
from django.contrib.auth.models import AbstractUser
from users.managers import CustomUserManager
from cloudinary.models import CloudinaryField


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    address = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=16, blank=True, null=True)
    profile_image = CloudinaryField('profile_image', blank=True, null=True)

    USERNAME_FIELD = 'email' # email instead of username
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email