from django.urls import path, include
from .views import paypal_view

urlpatterns = [
   path('paypal/ipn/', include('paypal.standard.ipn.urls')),
   path('paypal/register/', paypal_view, name='paypal_view')
]

