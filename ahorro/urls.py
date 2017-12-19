# Django libs:
from django.conf.urls import url

# Our web libs:
from ahorro import views

# URL definitions:
urlpatterns = [
    # Index:
    url(r'^$', views.index, name='index'),

    # Single plots:
    url(r'^plot/(?P<item>.+)/$', views.plot_item, name='plot_item'),

    # Data URLs:
    url(r'^item_data/(?P<item>.+)/$', views.item_data, name='item_data'),
]
