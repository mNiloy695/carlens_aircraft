from django.urls import path,include
from .views import CheckOutView,BookedModelView
from .webhook import stripe_webhook
urlpatterns = [
   path('payment/',CheckOutView.as_view(),name='checkout'),
   path('webhook/',stripe_webhook),
   path('list/',BookedModelView.as_view()),
]
