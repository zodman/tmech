from django.urls import path
from django.views.generic import TemplateView
from .views import *


urlpatterns = [
    path("", TemplateView.as_view(template_name="base.html"), name="index"),
    path("client/", client_list, name="client_list"),
    path("client/add", client_add, name="client_add"),
    path("client/search/", search_client, name="search_client"),
    path("client/delete/", delete_clients, name="delete_clients"),
    path("cars/", car_list, name="car_list"),
    path("cars/add/", car_add, name="car_add"),
    path("cars/edit/<int:pk>", car_edit, name="car_edit"),
    path("cars/delete/", delete_cars, name="delete_cars"),
    path("cars/search/", search_car, name="search_car"),
    path("cars/search/client/", search_car_clients, name="car_client_search"),
    path("service/search/car", service_search_cars, name="get_cars"),
    path("service/add", service_add, name="service_add"),
    path("service/", list_visit, name="list_visit"),
    

]
