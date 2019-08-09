from django.forms import modelform_factory
from core.models import Conf
from django.shortcuts import render

def setconf(request):
    ConfForm = modelform_factory(Conf, fields=("name","logo"))
    
    if request.POST:
        form = ConfForm(request.POST)
        if form.is_valid():
            pass
    else:
        form = ConfForm()
    context = {
        'form':form
    }
    return render(request, "core/conf/conf_form.html", context)