from django.shortcuts import render
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy as reverse
from django.contrib import messages
from ..models import Car


class CarList(ListView):
    model = Car
    paginate_by = 20

car_list = CarList.as_view()