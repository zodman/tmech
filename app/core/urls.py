from django.urls import path
from .views import *


urlpatterns = [
    path("client/", client_list, name="client_list"),
]
