from django.shortcuts import render
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy as reverse
from django.contrib import messages
from ..models import Client, Visit
from .utils import CreateIntercoolerMix
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _


__all__ = ["list_visit"]


class ListVisit(ListView):
    model = Visit
    template_name="core/visits/visit_list.html"

list_visit = ListVisit.as_view()