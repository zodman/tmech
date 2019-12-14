# CreateIntercoolerMix
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta

class IntercoolerMix:
    def form_valid(self, form):
        form = super().form_valid(form)
        url = self.get_success_url()
        resp = HttpResponse("")
        #messages.info(self.request, _("{} Added").format(self.model.__name__))
        resp["X-IC-Redirect"] = url
        #resp["Turbolinks-Location"] = url
        return resp

class CreateIntercoolerMix(IntercoolerMix, CreateView):
    ic_template = "form.html"

    def get_template_names(self):
        names = super().get_template_names()
        if self.request.is_ajax():
            return self.ic_template
        return names



class ListMix(object):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)

FILTERS = (
    ("all", _("All time")),
    ("m",_("This Month")),
    ("mm",_("Last Month")),
    ("t",_("Today")),
    ("y",_("Yesterday")),
    ("w",_("This Week"))
)

def filter_by_date(ds, q_time):
    now = timezone.now()
    if q_time == "m":
        ds = (ds.filter(reception_datetime__month=now.month)
                    .filter(reception_datetime__year=now.year))
    elif q_time =="mm":
        ds = ds.filter(
            reception_datetime__month=now.month-1,
            reception_datetime__year=now.year
        )
    elif q_time == "t":
        ds = ds.filter(reception_datetime__date=now.date())
    elif q_time == "y":
        ds = ds.filter(reception_datetime__date=now-timedelta(days=1))            
    elif q_time == "w":
        ds = ds.filter(reception_datetime__date=now-timedelta(days=7))            
    return ds