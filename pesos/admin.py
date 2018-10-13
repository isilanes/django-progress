# Django libs:
from django.contrib import admin

# Our libs:
from pesos.models import TimeInstant, Person, Weight


# Register your models here:
admin.site.register(TimeInstant)
admin.site.register(Person)
admin.site.register(Weight)
