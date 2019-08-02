from django.db import models
from django.utils.translation import gettext_lazy as _


class Personal(models.Model):
    name = models.CharField(max_length=200)
    position = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Client(models.Model):
    name = models.CharField(max_length=200, unique=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("created_at",)

    def __str__(self):
        return self.name

class Car(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
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
    status = models.CharField(max_length=10, choices=STATUS, default="o")
    car = models.ForeignKey(Car, on_delete=models.SET_NULL, null=True)
    reception_datetime = models.DateTimeField(help_text="YYYY-mm-dd HH:MM:SS")
    initial = models.TextField(_("Initial Diagnostic"))
    final = models.TextField(_("Final Diagnostic"))
    repairs = models.TextField(_("Repairs"))
    notes = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_status(self):
        return dict(self.STATUS).get(self.status)


class Item(models.Model):
    quantity = models.PositiveIntegerField()
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=15)
    diagnostic = models.ForeignKey("Diagnostic", on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total(self):
        return self.quantity*self.price

