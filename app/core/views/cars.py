from django.shortcuts import render
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy as reverse
from django.contrib import messages
from ..models import Car
from django.db.models import Q

def search_car_clients(request):
    search = request.GET.get("search")
    if search:
        cars = Car.objects.filter(
                Q(client__name__icontains=search)|
                Q(brand__icontains=search)|
                Q(model__icontains=search))
    else:
        cars = Car.objects.none()
    context = dict(object_list=cars)
    return render(request, "core/_cars.html", context)


class CarList(ListView):
    model = Car
    paginate_by = 20

car_list = CarList.as_view()
