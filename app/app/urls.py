from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView, RedirectView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

messages = TemplateView.as_view(template_name="messages.html")


urlpatterns = [
    path('admin/', admin.site.urls),
    path("admin/", include('loginas.urls')),
    path("messages/", messages, name="messages"),
    path("app/", include("core.urls")),
    path('accounts/', include('registration.backends.simple.urls')),
   path('', include('paypal_restrictor.urls')), # /paypal/


    path("", RedirectView.as_view(url="/app/dashboard/"), name="index" )
] + staticfiles_urlpatterns()
