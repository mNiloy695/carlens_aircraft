from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import OTP
User=get_user_model()
admin.site.register(User)
# Register your models here.

admin.site.register(OTP)
