from django.contrib import admin
from .models import Car, Client, Personal, Service, Diagnostic, Release
from .models import Quote, Item


admin.site.register(Car)
admin.site.register(Client)
admin.site.register(Personal)
admin.site.register(Service)
admin.site.register(Diagnostic)
admin.site.register(Release)
admin.site.register(Quote)
admin.site.register(Item)
