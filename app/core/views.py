from django.shortcuts import render
from django.views.generic import ListView
from .models import Client

class ClientList(ListView):
    model = Client
    paginate_by=3


client_list = ClientList.as_view()
