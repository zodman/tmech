from django.urls import path
from .views import *

urlpatterns = [
    path("client/", client_list, name="client_list"),
    path("client/add", client_add, name="client_add"),
    path("client/search/", search_client, name="search_client"),
    path("client/delete/", delete_clients, name="delete_clients"),

    path("cars/", car_list, name="car_list"),
]
