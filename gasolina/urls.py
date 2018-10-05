# Django libs:
from django.urls import path

# Our web libs:
from . import views


# Constants:
app_name = "gasolina"


# URL definitions:
urlpatterns = [
    # Index:
    path('', views.index, name='index'),

    # Single plots:
    path('plot/<item>', views.plot_item, name='plot_item'),

    # Data URLs:
    path('item_data/<item>', views.item_data, name='item_data'),
]
