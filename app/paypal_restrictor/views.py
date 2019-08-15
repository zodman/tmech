from django.shortcuts import render, redirect
from django.conf import settings
from .models import PaypalAccountBase
from django.http import HttpResponseRedirect
from paypal.standard.forms import PayPalPaymentsForm
from django.urls import reverse_lazy, reverse
from functools import wraps
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone


# decorator

def paypal_required(func):
    @wraps(func)
    def wrap(request, *args, **kwargs):
        if not hasattr(request.user, 'paypalaccount'):
            if 'redir' in kwargs:
                url = kwargs.get("redir")
            else:
                url = getattr(settings, "PAYPAL_RESTRICTOR_REDIRECT", reverse_lazy("paypal_view"))
            return redirect(url)
        return func(request, *args, **kwargs)
    return wrap


def paypal_view(request, *args, **kwargs):
    d_format = timezone.now().strftime("Ymd")
    invoice_id = "{}-{}".format(request.user.id, d_format)
    paypal_dict = {
        "business": getattr(settings, "PAYPAL_BUSSINES", "zodman-facilitator@gmail.com"),
        "amount": getattr(settings, "PAYPAL_COST", "20"),
        "item_name": getattr(settings, "PAYPAL_ITEM_NAME","paypal item"),
        "invoice": invoice_id,
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
   #    "return": request.build_absolute_uri(reverse_lazy('your-return-view')),
    #    "cancel_return": request.build_absolute_uri(reverse_lazy('your-cancel-view')),
        "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form}
    return render(request, "paypal_restrictor/payment.html", context)
