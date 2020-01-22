from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView, RedirectView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.i18n import i18n_patterns

messages = TemplateView.as_view(template_name="messages.html")
landing = TemplateView.as_view(template_name="landing.html")


urlpatterns = [
    path('admin/', admin.site.urls),
    path("admin/", include('loginas.urls')),
    path("messages/", messages, name="messages"),
    path("app/", include("core.urls")),
    path("accounts/profile/", RedirectView.as_view(url="/app/dashboard/"), name="index" ),
    path('accounts/', include('registration.backends.simple.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
    path('', include('paypal_restrictor.urls')), # /paypal/
    
    #path("", RedirectView.as_view(url="/app/dashboard/"), name="index" ),
    
] + i18n_patterns(path("", landing, name="landing"))  + staticfiles_urlpatterns()
