from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self,email,password=None,**extra_fields):
        if not email:
            raise ValueError("Email is required")
        phone=extra_fields.get('phone')
        if not phone:
            raise ValueError("Phone number is required")
        email=self.normalize_email(email)
        user=self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,email,password=None,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True")
        return self.create_user(email,password,**extra_fields)

class CustomUser(AbstractBaseUser,PermissionsMixin):
    email=models.EmailField(unique=True)
    full_name=models.CharField(max_length=100)
    phone=models.CharField(max_length=15,unique=True)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    date_joined=models.DateTimeField(auto_now_add=True)
    objects=CustomUserManager()
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['full_name','phone']
    def __str__(self):
        return self.email
    class Meta:
        ordering = ['-date_joined']

   
        

