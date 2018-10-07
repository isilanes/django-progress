# Django libs:
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView


# URL patterns:
urlpatterns = [
    # Admin view:
    path('admin/', admin.site.urls),

    # Main:
    path('', TemplateView.as_view(template_name="main_index.html"), name="main_index"),

    # Apps:
    path('gasolina/', include('gasolina.urls', namespace="gasolina")),
    path('ahorro/', include('ahorro.urls', namespace="ahorro")),
    path('books/', include('books.urls', namespace="books")),
]
