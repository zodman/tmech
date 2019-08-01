from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView
from django.urls import reverse_lazy as reverse
from django.contrib import messages
from ..models import Client, Diagnostic, Car
from .utils import CreateIntercoolerMix
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
from django.forms import modelform_factory
from django.utils import timezone

__all__ = ["service_list","service_add","service_search_cars", "service_detail"]

def service_search_cars(request):
    ServiceForm = modelform_factory(Diagnostic, fields=("__all__"))
    f = ServiceForm(initial={'reception_datetime': timezone.now()})
    client_id = request.GET.get("client_id")
    f.fields["car"].queryset=Car.objects.filter(client__id=client_id)
    context = {
        'form':f
    }
    r = render(request, "core/service/_search_cars.html",context)
    r["X-IC-Script"]="$('button').show()"
    return r


class ServiceDetail(DetailView):
    model = Diagnostic
    template_name="core/service/detail.html"

service_detail = ServiceDetail.as_view()

class ListVisit(ListView):
    model = Diagnostic
    template_name = "core/service/service_list.html"

service_list = ListVisit.as_view()


class ServiceAdd(CreateIntercoolerMix):
    model = Diagnostic
    fields = ["car","reception_datetime", "initial", "final", "repairs", "notes"]
    success_url = reverse("service_list")
    template_name = "core/service/service_form.html"
    initial={'reception_datetime': timezone.now()}

service_add = ServiceAdd.as_view()
