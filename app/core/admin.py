from django.contrib import admin
from .models import Car, Client
from .models import  Item, Diagnostic


admin.site.register(Car)
admin.site.register(Client)

admin.site.register(Diagnostic)

admin.site.register(Item)
