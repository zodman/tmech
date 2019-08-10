from django.views.generic import TemplateView
from core.models import Diagnostic, Client
from django.contrib.auth.decorators import login_required
from .utils import filter_by_date


class Dashboard(TemplateView):
    template_name="core/dashboard.html"

    def profit(self, ds):
        return sum([d.total() for d in ds])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ds = Diagnostic.objects.filter(user=self.request.user)
        q_time = self.request.GET.get("search_time","m")
        if q_time:
            ds = filter_by_date(ds, q_time)
        context.update({
            'raw_services':ds,
            'services': ds[0:10],
            'profit': self.profit(ds),
            'clients': Client.objects.filter(user=self.request.user)[0:10]
        })
        return context

dashboard = login_required(Dashboard.as_view())
