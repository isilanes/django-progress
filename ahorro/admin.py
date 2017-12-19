# Django libs:
from django.contrib import admin

# Our libs:
from ahorro.models import TimeInstant, Account, Amount

# Register your models here:
admin.site.register(TimeInstant)
admin.site.register(Account)
admin.site.register(Amount)
