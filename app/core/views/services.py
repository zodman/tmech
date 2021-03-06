from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.urls import reverse_lazy as reverse
from django.contrib import messages
from django.db import models
from ..models import Client, Diagnostic, Car, Item
from .utils import CreateIntercoolerMix, IntercoolerMix, ListMix, filter_by_date, FILTERS
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
from django.forms import modelform_factory
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from paypal_restrictor.views import paypal_required
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

decors = [
    login_required,
    paypal_required,
]


__all__ = ["service_list","service_add","service_search_cars",
           "service_detail","service_edit","service_change_status", 
           "service_add_item","service_delete_item", "service_search"]



@method_decorator(decors, name="dispatch")
class ListVisit(ListMix, ListView):
    model = Diagnostic
    paginate_by = 5
    template_name = "core/service/service_list.html"

    def get_template_names(self):
        if self.request.META.get("HTTP_X_IC_Request".upper()):
            self.template_name = "core/service/_visit.html"
        return super().get_template_names()

    def get_queryset(self):
        qs = super().get_queryset()
        status = self.request.GET.get("status")
        t = self.request.GET.get("search_time")
        if status:
            qs = qs.filter(status=status)
        if t:
          qs= filter_by_date(qs, t)
        return qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        status = self.request.GET.get("status")
        t = self.request.GET.get("search_time")
        if status or t:
            context["status"] = status 
            context["search_time"] = t
        context["FILTERS"] = FILTERS
        return context
    

service_list = login_required(ListVisit.as_view())

@login_required
@paypal_required
def service_search(request):
    q = request.GET.get("search")
    status = request.GET.get("status")
    t = request.GET.get("search_time")
    if status or t:
        resp = HttpResponse()
        url = reverse("service_list")
        resp["X-IC-Redirect"] = f"{url}?status={status}&search_time={t}"
        return resp
    ds = Diagnostic.objects.filter(user=request.user)
    if q:
        ds = ds.filter(
            models.Q(car__brand__icontains=q)|
            models.Q(car__model__icontains=q)|
            models.Q(car__client__name__icontains=q)
        ).distinct()
    object_list = ds
    ctx = {'object_list': object_list}
    return render(request, "core/service/_visit.html", ctx)

@login_required
@paypal_required
def service_change_status(request, pk):
    service = Diagnostic.objects.filter(user=request.user).get(id=pk)
    if request.POST:
        status = request.POST.get("status")
        if service.total() == 0:
            messages.error(request, _("Status not change, total empty"))
            r = HttpResponse()
            r["X-IC-Redirect"] = reverse("service_detail", kwargs={'pk': service.id})
            service.status = Diagnostic.STATUS[0][0]
            service.save()
            return r
        if status:
            service.status = status
            service.save()
            messages.info(request, _("status change to {}").format(service.get_status()))
            r = HttpResponse()
            r["X-IC-Redirect"] = reverse("service_detail", kwargs={'pk': service.id})
            return r




@login_required
@paypal_required
def service_search_cars(request):
    ServiceForm = modelform_factory(Diagnostic, fields=["car","reception_datetime", "initial", "final", "repairs", "notes"])
    f = ServiceForm(initial={'reception_datetime': timezone.now()})
    client_id = request.GET.get("client_id")
    f.fields["car"].queryset=Car.objects.filter(
            client__id=client_id,
            user=request.user,
            )
    context = {
        'form':f,
    }
    context.update(dict(WIDGET_REQUIRED_CLASS="is-primary",WIDGET_ERROR_CLASS="is-danger"))
    r = render(request, "core/service/_search_cars.html",context)
    r["X-IC-Script"]="$('button').show()"
    return r



@method_decorator(decors, name="dispatch")
class ServiceDetail(ListMix, DetailView):
    model = Diagnostic
    template_name="core/service/detail.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ItemForm = modelform_factory(Item, fields=["quantity","description","price", 'diagnostic'])
        form = ItemForm(initial={'diagnostic': self.object})
        ctx.update({'form':form})
        return ctx


service_detail = login_required(ServiceDetail.as_view())

import django_filters

class ServiceFilter(django_filters.FilterSet):
    class Meta:
        model = Diagnostic
        fields = ["reception_datetime",]




@method_decorator(decors, name="dispatch")
class ServiceAdd(ListMix, CreateIntercoolerMix):
    model = Diagnostic
    fields = ["car","reception_datetime", "initial", "final", "repairs", "notes"]
    success_url = reverse("service_list")
    template_name = "core/service/service_form.html"
    initial={'reception_datetime': timezone.now()}

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        form = super().form_valid(form)
        url = self.get_success_url()
        resp = HttpResponse("")
        #messages.info(self.request, _("{} Added").format(self.model.__name__))
        resp["X-IC-Redirect"] = url
        #resp["Turbolinks-Location"] = url
        return resp


service_add = login_required(ServiceAdd.as_view())


@method_decorator(decors, name="dispatch")
class ServiceEdit(ListMix, IntercoolerMix, UpdateView):
    model = Diagnostic
    template_name="core/service/_service_form.html"
    fields = ["reception_datetime","initial","final","repairs","notes"]

    def form_valid(self, form):
        messages.info(self.request, _("Service edited"))
        return super().form_valid(form)
    def get_success_url(self):
        return reverse("service_detail", kwargs={'pk': self.object.id})

service_edit = login_required(ServiceEdit.as_view())



@login_required
@paypal_required
def service_add_item(request, pk):
    service = Diagnostic.objects.get(id=pk)
    ctx = {}
    ItemForm = modelform_factory(Item, fields=["quantity","description","price"])
    
    if request.POST:
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.diagnostic = service
            item.user = request.user
            item.save()
            messages.info(request,_("Item added"))
            # resp = HttpResponse()
            # resp["X-IC-Redirect"] = reverse("service_detail", kwargs={'pk': service.id})
            # return resp
        ctx = {
        'object':service,
        'form':form}
        return render(request, "core/service/_quote.html", ctx)
    else:
        form = ItemForm()
    ctx.update({
        'form':form,
        'object':service,
    })
    return render(request, "core/service/_quote.html", ctx)


@login_required
@paypal_required
def service_delete_item(request, pk):
    item = Item.objects.filter(user=request.user).get(id=pk)
    service = item.diagnostic
    item.delete()
    messages.info(request, _("Item deleted"))
    ItemForm = modelform_factory(Item, fields=["quantity","description","price"])
    form = ItemForm()
    ctx={
        'form':form,
        'object':service,
    }
    return render(request, "core/service/_quote.html", ctx)