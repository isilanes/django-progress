# Django libs:
from django.db import models
from django.utils import timezone

# Classes:
class PlotState(models.Model):
    """The values of all plot variables."""

    # Attributes:
    timestamp = models.DateTimeField("Timestamp", default=timezone.now)
    total_kms = models.IntegerField("Total kilometres", default=0)
    partial_kms = models.FloatField("Partial kilometres", default=0)
    litres = models.FloatField("Litres", default=0)
    price = models.FloatField("Price (eur/L)", default=0)
    
    # Public functions:
    def plottable_attributes(self):
        return ["total_kms", "partial_kms", "litres", "price"]


    # Special functions:
    def __str__(self):
        return "{s.timestamp}".format(s=self)

    def __unicode__(self):
        return self.__str__()

class VariableConfig(models.Model):
    """The configuration parameters for a variable."""

    # Attributes:
    name = models.CharField("Name", default="name", max_length=50)
    long_name = models.CharField("Long name", default="long_name", max_length=100)
    style = models.CharField("Plot style", default="r", max_length=50)
    objective = models.IntegerField("Objective", default=1)

    # Special functions:
    def __str__(self):
        return self.long_name

    def __unicode__(self):
        return self.__str__()

