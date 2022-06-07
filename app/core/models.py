""""
Database models.
"""
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

# Create your models here.

class UserManager(BaseUserManager):
    """Manager for users."""
    #**extra_fields can provid keyword arguments
    # can pass name as extra field, which will be automatically created when the user models is created 
    # the benefit is that every time you update it do not need to change the code 
    # will pass to the new model 

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # assigbne the user manager to our custom user class 
    # 
    objects = UserManager()
    # use as auth 
    USERNAME_FIELD = 'email'