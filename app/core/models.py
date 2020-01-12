from django.db import models
from django.utils.translation import gettext_lazy as _
from .managers import ServiceQuerySet 
from django.contrib.auth.models import User
from paypal_restrictor.models import PaypalAccountBase
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

class PaypalAccount(PaypalAccountBase):
    def __str__(self):
        return f"{self.user.username}"

class Conf(models.Model):
    user = models.OneToOneField(User, verbose_name=_("user"), on_delete=models.CASCADE)
    name = models.CharField(max_length=200, help_text=_("Company name"))
    logo = models.URLField(help_text=_("Set url for a image"))

    def __str__(self):
        return "{}".format(self.user)


class Client(models.Model):
    name = models.CharField(max_length=200, unique=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("created_at",)

    def __str__(self):
        return self.name


    def last_service(self):
        cars_ids = self.car_set.all().values_list("id", flat=True)
        result = Diagnostic.objects.filter(car__id__in=cars_ids).aggregate(max_date=models.Max("reception_datetime"))
        if result:
            return result.get("max_date")


class Car(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("client","brand","model","year")
        ordering = ("-id",)
    def __str__(self):
        return f"{self.brand} -- {self.model} -- {self.year}"


class Diagnostic(models.Model):
    STATUS = (
        ("o",_("Open")),
        ("c",_("Completed")),
        ("p",_("Paid")),
    )
    STATUS_COLOR =  (
        ("o","info"),
        ("c",'success'),
        ("p","danger"),
    )
    status = models.CharField(max_length=10, choices=STATUS, default="o")
    car = models.ForeignKey(Car, on_delete=models.SET_NULL, null=True)
    reception_datetime = models.DateTimeField(help_text="YYYY-mm-dd HH:MM:SS")
    initial = models.TextField(_("Initial Diagnostic"))
    final = models.TextField(_("Final Diagnostic"),null=True, blank=True)
    repairs = models.TextField(_("Repairs"),null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ServiceQuerySet.as_manager()

    class Meta:
        ordering = ("-reception_datetime", "status")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Call the "real" save() method.

    def get_status(self):
        return dict(self.STATUS).get(self.status)
    def get_color(self):
        return dict(self.STATUS_COLOR).get(self.status)
    def total(self):
        r = self.item_set.values("quantity","price")
        all = [i["quantity"]*i["price"] for i in r]
        return sum(all)


class Item(models.Model):
    quantity = models.PositiveIntegerField()
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=15)
    diagnostic = models.ForeignKey("Diagnostic", on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total(self):
        return self.quantity*self.price


# PAYPAL

from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received

def show_me_the_money(sender, **kwargs):
    ipn_obj = sender
    bussines_email = getattr(settings, "PAYPAL_BUSSINES", "zodman-facilitator@gmail.com")
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        # WARNING !
        # Check that the receiver email is the same we previously
        # set on the `business` field. (The user could tamper with
        # that fields on the payment form before it goes to PayPal)
        if ipn_obj.receiver_email != bussines_email:
            # Not a valid payment
            return

        # ALSO: for the same reason, you need to check the amount
        # received, `custom` etc. are all what you expect or what
        # is allowed.

        price = getattr(settings, "PAYPAL_COST", 20)

        if float(ipn_obj.mc_gross) == float(price):
            invoice = ipn_obj.invoice
            user_id  = invoice.split("-")[0]
            days = getattr(settings,"PAYPAL_DAYS_EXPIRED",30)
            now = timezone.now() + timedelta(days=days)
            user = User.objects.get(id=user_id)
            account, _  = PaypalAccount.objects.get_or_create(user=user)
            account.expire = now
            account.save()
    else:
        ...
valid_ipn_received.connect(show_me_the_money)













