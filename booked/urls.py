from django.urls import path,include
from .views import CheckOutView
from .webhook import stripe_webhook
urlpatterns = [
   path('payment/',CheckOutView.as_view(),name='checkout'),
   path('webhook/',stripe_webhook)
]
