from django.shortcuts import render
from django.views.generic import ListView
from .models import Client

class ClientList(ListView):
    model = Client


client_list = ClientList.as_view()
