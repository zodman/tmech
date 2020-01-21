from django.forms import modelform_factory
from core.models import Conf
from django.shortcuts import render
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from paypal_restrictor.views import paypal_required
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

decors = [
    login_required,
    # paypal_required,
]

@login_required
@paypal_required
def setconf(request):
    ConfForm = modelform_factory(Conf, fields=("name","logo","address"))
    try:
        instance = getattr(request.user,"conf")
    except Conf.DoesNotExist:
        instance = None
    if request.POST:
        if instance:
            form = ConfForm(request.POST, instance=instance)
        else:
            form  = ConfForm(request.POST)
        if form.is_valid():
            instance=form.save(commit=False)
            instance.user = request.user
            instance.save()
            messages.info(request, _("Conf set"))
    else:
        form = ConfForm(instance=instance)
    context = {
        'form':form
    }
    return render(request, "core/conf/conf_form.html", context)