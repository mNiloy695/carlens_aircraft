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
    country_code=models.CharField(max_length=5,default="BB")
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

   
        

from django.contrib.auth import get_user_model
User= get_user_model()

class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    type=models.CharField(max_length=20,choices=[('registration','registration'),('password_reset','password_reset')],default='registration')
    
    def is_expired(self):
        from django.utils import timezone
        expiration_time = self.created_at + timezone.timedelta(minutes=10)
        return timezone.now() > expiration_time

    def __str__(self):
        return f"OTP for {self.user.email} - {self.code}"






class UserProfile(models.Model):
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE,related_name='profile')
    full_name=models.CharField(max_length=50)
    avatar=models.ImageField(upload_to='profile',null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)