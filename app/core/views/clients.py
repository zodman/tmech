from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy as reverse
from django.contrib import messages
from ..models import Client
from .utils import CreateIntercoolerMix, IntercoolerMix
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required


__all__ = ["search_client", "client_list",
           "client_add", "delete_clients", "edit_client"]


class EditClient(IntercoolerMix, UpdateView):
    model = Client
    fields = ("__all__")
    template_name="core/client/client_form.html"
    def get_success_url(self):
        url = reverse("client_list")
        return url

edit_client = login_required(EditClient.as_view())

@login_required
def delete_clients(request):
    ids = request.POST.getlist("ids")
    if ids:
        Client.objects.filter(id__in=ids).delete()
        resp = HttpResponse("")
        messages.info(request, _("Clients deleted"))
        resp["X-IC-Redirect"] = reverse("client_list")
        return resp

class ClientAdd(CreateIntercoolerMix):
    model = Client
    fields = ("__all__")
    success_url = reverse("client_list")
    template_name="core/client/client_form.html"


client_add = login_required(ClientAdd.as_view())

@login_required
def search_client(request):
    search = request.GET.get("search")
    if search:
        qs = Client.objects.filter(name__icontains=search)
    else:
        qs = Client.objects.none()
    context = {'object_list': qs}
    return render(request, "core/client/_client.html", context)


class ClientList(ListView):
    model = Client
    paginate_by = 20
    template_name="core/client/client_list.html"


client_list = login_required(ClientList.as_view())
