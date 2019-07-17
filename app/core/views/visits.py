from django.shortcuts import render
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy as reverse
from django.contrib import messages
from ..models import Client, Service, Diagnostic
from .utils import CreateIntercoolerMix
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
from django.forms import modelform_factory


__all__ = ["list_visit","service_add"]


class ListVisit(ListView):
    model = Service
    template_name = "core/visits/visit_list.html"

list_visit = ListVisit.as_view()


class ServiceAdd(CreateIntercoolerMix):
    model = Diagnostic
    fields = ["reception_datetime", "initial", "final", "repairs", "notes"]
    exclude = ("service",)
    template_name = "core/service/service_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        DiagnosticForm = modelform_factory(Service, exclude=("service",))
        form2 = DiagnosticForm()
        context.update({
            'form2': form2
        })
        return context



service_add = ServiceAdd.as_view()
