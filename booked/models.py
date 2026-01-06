from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.
User=get_user_model()

PAYMENT_STATUS=(
    ('held','held'),
    ('refund','refund'),
    ('paid','paid'),
    ('unpaid','unpaid')
)

BOOKING_STATUS=(
    ('pending','pending'),
    ('confirmed','confirmed'),
)

class BookedModel(models.Model):
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name='bookings')
    booking_id=models.CharField(max_length=200,null=True,blank=True)
    payment_id=models.CharField(max_length=200,null=True,blank=True)
    operator_id=models.CharField(max_length=100)
    aircraft_id=models.CharField(max_length=100)
    flight_date=models.DateTimeField()
    passengers=models.IntegerField()
    form=models.CharField(max_length=100)
    to=models.CharField(max_length=100)
    amount=models.BigIntegerField(default=0)
    currency=models.CharField(max_length=100,null=True,blank=True)
    booking_status=models.CharField(max_length=100,choices=BOOKING_STATUS,default='pending')
    payment_status=models.CharField(max_length=100,choices=PAYMENT_STATUS,default='unpaid')
    created_at=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_at=models.DateTimeField(auto_now=True,blank=True,null=True)


    class Meta:
        ordering=['-created_at']
    

