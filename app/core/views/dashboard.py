from django.views.generic import TemplateView
from core.models import Diagnostic, Client


class Dashboard(TemplateView):
    template_name="core/dashboard.html"

    def profit(self, ds):
        return sum([d.total() for d in ds])
            

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ds = Diagnostic.objects.all()
        context.update({
            'services': ds,
            'profit': self.profit(ds),
            'clients': Client.objects.all()
        })
        return context
dashboard = Dashboard.as_view()

#TODO: mejorar el dashboard