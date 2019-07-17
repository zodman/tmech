from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView, RedirectView

messages = TemplateView.as_view(template_name="messages.html")


urlpatterns = [
    path('admin/', admin.site.urls),
    path("messages/", messages, name="messages"),
    path("app/", include("core.urls")),
    path("", RedirectView.as_view(url="/app/"), name="index" )
]
