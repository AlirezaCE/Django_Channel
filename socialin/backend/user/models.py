from django.db import models
from django.core.validators import validate_email
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
) 
from django.core.validators import validate_email


class UserManager(BaseUserManager):
    
    
    def create_user(self, username, email=None, phone=None, password=None):
        if not username:
            raise ValueError("username is required.")
        if not phone and not email:
            raise ValueError("either phone or email is required.")        
        user = self.model(username=username, email=email, phone=phone)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email=None, phone=None, password=None):
        user = self.create_user(username, email, phone, password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(unique=True, max_length=32, null = True, blank= True, verbose_name='username')
    password = models.CharField(unique=False, max_length=128, null=False, blank=False, verbose_name='password')
    email = models.EmailField(max_length=32,unique=True, blank=True, null=True, verbose_name='Email for signin', validators=[validate_email])
    phone = models.CharField(max_length=32, unique=True, blank=True, null=True, verbose_name='Phone number')
    is_staff = models.BooleanField(default=False)
    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = ['username']

    

    objects = UserManager()
    
    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural = "Users"