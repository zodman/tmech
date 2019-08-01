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


class Service(models.Model):
    car = models.ForeignKey(Car, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Diagnostic(models.Model):
    service = models.ForeignKey("Service", verbose_name=_("Service"), on_delete=models.CASCADE)
    reception_datetime = models.DateTimeField(help_text="YYYY/mm/dd HH:MM")
    initial = models.TextField(_("Initial Diagnostic"))
    final = models.TextField(_("Final Diagnostic"))
    repairs = models.TextField(_("Repairs"))
    notes = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Item(models.Model):
    quantity = models.PositiveIntegerField()
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=8)
    quote = models.ForeignKey("Quote", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Quote(models.Model):
    name = models.CharField(_("name"), max_length=200)
    client = models.ForeignKey("Client", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class Release(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    quotes = models.ManyToManyField("Quote")
