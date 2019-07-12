from django.shortcuts import render
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy as reverse
from django.contrib import messages
from django.http import HttpResponse
from ..models import Car, Client
from django.db.models import Q
from .utils import CreateIntercoolerMix
import json
__all__ = ["search_car_clients", "search_car", "car_list", "car_add"]


class CarAdd(CreateIntercoolerMix):
    model = Car
    fields = ("brand","model","year")
#    fields = ("__all__")

    def form_valid(self, form):
        client_id = self.request.POST.get("client_id")
        if not client_id:
            form.add_error(None, "Missing client")
            return super().form_invalid(form)
        else:
            instance = form.save(commit=False)
            instance.client = Client.objects.get(id=client_id)
            instance.save()
        return super().form_valid()

car_add = CarAdd.as_view()


def search_car(request):
    search = request.GET.get("search")
    if search:
        cars = Car.objects.filter(
            Q(client__name__icontains=search) | Q(brand__icontains=search)
            | Q(model__icontains=search))
    else:
        cars = Car.objects.none()
    context = dict(object_list=cars)
    return render(request, "core/_cars.html", context)


def search_car_clients(request):
    search = request.GET.get("search")
    if search:
        cars = Client.objects.filter(Q(name__icontains=search))
    else:
        cars = Client.objects.none()

    resp = [{'value': car.id, 'label': car.name} for car in cars]
    return HttpResponse(json.dumps(resp))


class CarList(ListView):
    model = Car
    paginate_by = 20


car_list = CarList.as_view()
