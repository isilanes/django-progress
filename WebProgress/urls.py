# Django libs:
from django.contrib import admin
from django.conf.urls import url, include
from django.views.generic import TemplateView

# Our libs:
from . import settings


# URL patterns:
urlpatterns = [
    url(r'^admin/', admin.site.urls),

    # Main:
    url(r'^$', TemplateView.as_view(template_name=settings.MAIN_INDEX), name="main_index"),

    # gasolina web:
    url(r'^gasolina/', include('gasolina.urls', namespace="gasolina")),

    # ahorro web:
    url(r'^ahorro/', include('ahorro.urls', namespace="ahorro")),
]
