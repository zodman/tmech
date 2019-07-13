# CreateIntercoolerMix
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView
from django.contrib import messages

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
        messages.info(self.request, _("{} Added").format(self.model.__name__))
        resp["X-IC-Redirect"] = url
        return resp

