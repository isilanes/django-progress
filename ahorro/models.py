# Django libs:
from django.db import models
from django.utils import timezone

# Classes:
class TimeInstant(models.Model):
    """A datetime, an instant in time."""

    timestamp = models.DateTimeField("Timestamp", default=timezone.now)

    # Public properties:
    @property
    def total_amount(self):
        """Sum of all amounts that have this TimeInstant as timestamp."""

        return sum([a.value for a in Amount.objects.filter(when=self)])

    
    # Special methods:
    def __unicode__(self):
        return self.__str__()

    def __str__(self):
        return self.timestamp.strftime("%Y-%m-%d %H:%M:%S")

class Account(models.Model):
    """The configuration parameters for an account."""

    name = models.CharField("Name", default="name", max_length=50)
    color = models.CharField("Color", default="#000000", max_length=7)
    icon = models.CharField("Icon", default="default.png", max_length=100)

    # Special methods:
    def __unicode__(self):
        return self.__str__()

    def __str__(self):
        return self.name

class Amount(models.Model):
    """An amount of time (for a given Account, on a given TimeInstant."""

    value = models.FloatField("Amount", default=0.0)
    when = models.ForeignKey(TimeInstant)
    account = models.ForeignKey(Account)

    # Special methods:
    def __unicode__(self):
        return self.__str__()

    def __str__(self):
        return "{s.value:.2f} eur for {s.account} at {s.when}".format(s=self)

