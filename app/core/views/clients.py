from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy as reverse
from django.contrib import messages
from ..models import Client
from .utils import CreateIntercoolerMix, IntercoolerMix, ListMix
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from paypal_restrictor.views import paypal_required
from django.utils.decorators import method_decorator

decors = [
    login_required,
    paypal_required,
]



__all__ = ["search_client", "client_list",
           "client_add", "delete_clients", "edit_client"]


@method_decorator(decors, name="dispatch")
class EditClient(IntercoolerMix, ListMix, UpdateView):
    model = Client
    fields = ("__all__")
    template_name="core/client/client_form.html"

    def get_success_url(self):
        url = reverse("client_list")
        return url

edit_client =EditClient.as_view()

@login_required
@paypal_required
def delete_clients(request):
    ids = request.POST.getlist("ids")
    if ids:
        qs = Client.objects.filter(user=request.user)
        qs.filter(id__in=ids).delete()
        resp = HttpResponse("")
        messages.info(request, _("Clients deleted"))
        resp["X-IC-Redirect"] = reverse("client_list")
        return resp

@method_decorator(decors, name="dispatch")
class ClientAdd(CreateIntercoolerMix):
    model = Client
    fields = ("name","phone", "email",)
    success_url = reverse("client_list")
    template_name = "core/client/client_form.html"

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()
        messages.info(self.request, _("Client added"))
        return super().form_valid(form)


client_add =ClientAdd.as_view()

@login_required
@paypal_required
def search_client(request):
    search = request.GET.get("search")
    qs = Client.objects.filter(user=request.user)
    if search:
        qs = qs.filter(name__icontains=search)
    else:
        qs = Client.objects.none()
    context = {'object_list': qs}
    return render(request, "core/client/_client.html", context)


@method_decorator(decors, name="dispatch")
class ClientList(ListMix, ListView):
    model = Client
    paginate_by = 20
    template_name="core/client/client_list.html"


client_list =ClientList.as_view()
