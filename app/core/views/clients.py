from django.shortcuts import render
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy as reverse
from django.contrib import messages
from ..models import Client
# CreateIntercoolerMix
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _



__all__ = ["search_client", "client_list", "client_add", "delete_clients"]


class CreateIntercoolerMix(CreateView):
    ic_template = "form.html"

    def get_template_names(self):
        names = super().get_template_names()
        if self.request.is_ajax():
            return self.ic_template
        return names

    def form_valid(self, form):
        form = super().form_valid(form)
        url = self.get_success_url()
        resp = HttpResponse("")
        messages.info(self.request, _("Contact added"))
        resp["X-IC-Redirect"] = url
        return resp


def delete_clients(request):
    ids = request.POST.getlist("ids")
    Client.objects.filter(id__in=ids).delete()
    resp = HttpResponse("")
    messages.info(request, _("Clients deleted"))
    resp["X-IC-Redirect"] = reverse("client_list")
    return resp



class ClientAdd(CreateIntercoolerMix):
    model = Client
    fields = ("__all__")
    success_url = reverse("client_list")


client_add = ClientAdd.as_view()


def search_client(request):
    search = request.GET.get("search")
    if search:
        qs = Client.objects.filter(name__icontains=search)
    else:
        qs = Client.objects.none()
    context = {'object_list': qs}
    return render(request, "core/_client.html", context)


class ClientList(ListView):
    model = Client
    paginate_by = 20


client_list = ClientList.as_view()
