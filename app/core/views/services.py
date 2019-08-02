from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.urls import reverse_lazy as reverse
from django.contrib import messages
from django.db import models
from ..models import Client, Diagnostic, Car, Item
from .utils import CreateIntercoolerMix, IntercoolerMix
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
from django.forms import modelform_factory
from django.utils import timezone

__all__ = ["service_list","service_add","service_search_cars",
           "service_detail","service_edit","service_change_status", 
           "service_add_item","service_delete_item", "service_search"]

def service_search(request):
    q = request.GET.get("search")
    status = request.GET.get("status")
    ds = Diagnostic.objects.all()
    if q:
        ds = ds.filter(
            models.Q(car__brand__icontains=q)|
            models.Q(car__model__icontains=q)|
            models.Q(car__client__name__icontains=q)
        ).distinct()
    
    if status:
        ds = ds.filter(status=status)
    ctx = {'object_list': ds}
    return render(request, "core/service/_visit.html", ctx)


def service_change_status(request, pk):
    service = Diagnostic.objects.get(id=pk)
    if request.POST:
        status = request.POST.get("status")
        if status:
            service.status = status
            service.save()
            messages.info(request, _("status change to {}").format(service.get_status()))
            r = HttpResponse()
            r["X-IC-Redirect"] = reverse("service_detail", kwargs={'pk': service.id})
            return r

def service_search_cars(request):
    ServiceForm = modelform_factory(Diagnostic, fields=["car","reception_datetime", "initial", "final", "repairs", "notes"])
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

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ItemForm = modelform_factory(Item, fields=["quantity","description","price", 'diagnostic'])
        form = ItemForm(initial={'diagnostic': self.object})
        ctx.update({'form':form})
        return ctx


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


class ServiceEdit(IntercoolerMix, UpdateView):
    model = Diagnostic
    template_name="core/service/_service_form.html"
    fields = ["reception_datetime","initial","final","repairs","notes"]

    def form_valid(self, form):
        messages.info(self.request, _("Service edited"))
        return super().form_valid(form)
    def get_success_url(self):
        return reverse("service_detail", kwargs={'pk': self.object.id})

service_edit = ServiceEdit.as_view()




def service_add_item(request, pk):
    service = Diagnostic.objects.get(id=pk)
    ctx = {}
    ItemForm = modelform_factory(Item, fields=["quantity","description","price"])
    
    if request.POST:
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.diagnostic = service
            item.save()
            messages.info(request,_("Item added"))
            resp = HttpResponse()
            resp["X-IC-Redirect"] = reverse("service_detail", kwargs={'pk': service.id})
            return resp
    else:
        form = ItemForm()
    ctx.update({
        'form':form,
        'object':service,
    })
    return render(request, "core/service/_quote.html", ctx)



def service_delete_item(request, pk):
    item = Item.objects.get(id=pk)
    item.delete()
    messages.info(request, _("Item deleted"))
    resp =HttpResponse()
    resp["X-IC-Remove"] ="1s"
    return resp