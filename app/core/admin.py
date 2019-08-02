from django.contrib import admin
from .models import Car, Client, Personal
from .models import  Item, Diagnostic


admin.site.register(Car)
admin.site.register(Client)
admin.site.register(Personal)

admin.site.register(Diagnostic)

admin.site.register(Item)
