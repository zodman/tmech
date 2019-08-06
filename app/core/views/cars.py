from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy as reverse
from django.contrib import messages
from django.http import HttpResponse
from ..models import Car, Client
from django.db.models import Q
from .utils import CreateIntercoolerMix
import json
from django.utils.translation import gettext_lazy as _
from django.db.utils import IntegrityError

from django.contrib.auth.decorators import login_required
from django.db import transaction

__all__ = [
    "search_car_clients", "search_car", "car_edit", "car_list", "car_add",
    "delete_cars"
]


class CarAdd(CreateIntercoolerMix):
    model = Car
    fields = ("brand", "model", "year")
    success_url = reverse("car_list")
    template_name = "core/car/car_form.html"

    def form_valid(self, form):
        client_id = self.request.POST.get("client_id")
        if not client_id:
            form.add_error(None, _("Missing client"))
            return super().form_invalid(form)
        else:
            instance = form.save(commit=False)
            instance.client = Client.objects.get(id=client_id)
            instance.user = self.request.user

            if (Car.objects.filter(
                    brand=instance.brand, model=instance.model,
                    year=instance.year).exists()):
                form.add_error(None, _("client with brand,model,year exists"))
                return super().form_invalid(form)

            try:
                instance.save()
            except IntegrityError:
                form.add_error(None, _("client with brand,model,year exists"))
                return super().form_invalid(form)
        return super().form_valid(form)


car_add = login_required(CarAdd.as_view())


class CarEdit(CarAdd, UpdateView):
    model = Car
    fields = ("brand", "model", "year")
    #    fields = ("__all__")
    success_url = reverse("car_list")
    template_name = "core/car/car_form.html"


car_edit = login_required(CarEdit.as_view())


@login_required
def search_car(request):
    search = request.GET.get("search")
    if search:
        cars = Car.objects.filter(
            Q(client__name__icontains=search) | Q(brand__icontains=search)
            | Q(model__icontains=search))
    else:
        cars = Car.objects.none()
    context = dict(object_list=cars)
    return render(request, "core/car/_cars.html", context)


@login_required
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
    template_name = "core/car/car_list.html"


car_list = login_required(CarList.as_view())


@login_required
def delete_cars(request):
    ids = request.POST.getlist("ids")
    Car.objects.filter(id__in=ids).delete()
    resp = HttpResponse("")
    messages.info(request, _("cars deleted"))
    resp["X-IC-Redirect"] = reverse("car_list")
    return resp
