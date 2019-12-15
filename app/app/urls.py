from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView, RedirectView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


messages = TemplateView.as_view(template_name="messages.html")
landing = TemplateView.as_view(template_name="landing.html")


urlpatterns = [
    path('admin/', admin.site.urls),
    path("admin/", include('loginas.urls')),
    path("messages/", messages, name="messages"),
    path("app/", include("core.urls")),
     path("accounts/profile/", RedirectView.as_view(url="/app/dashboard/"), name="index" ),
    path('accounts/', include('registration.backends.simple.urls')),
    path("", landing, name="landing"),
    path('', include('paypal_restrictor.urls')), # /paypal/
    path("", landing, name="landing"),
    #path("", RedirectView.as_view(url="/app/dashboard/"), name="index" ),
    
] + staticfiles_urlpatterns()
