# Django libs:
from django.db import models
from django.utils import timezone


# Classes:
class TimeInstant(models.Model):
    """A datetime, an instant in time."""

    timestamp = models.DateTimeField("Timestamp", default=timezone.now)

    # Special methods:
    def __unicode__(self):
        return self.__str__()

    def __str__(self):
        return self.timestamp.strftime("%Y-%m-%d %H:%M:%S")


class Person(models.Model):
    """Configuration for a Person."""

    name = models.CharField("Name", default="name", max_length=50)

    # Public properties:
    @property
    def graphite_name(self):
        name = self.name.lower()
        name = name.replace("ñ", "n")

        return name

    # Special methods:
    def __unicode__(self):
        return self.__str__()

    def __str__(self):
        return self.name


class Weight(models.Model):
    """An amount of kilograms (for a given Person, on a given TimeInstant)."""

    value = models.FloatField("Weight", default=0.0)
    when = models.ForeignKey(TimeInstant, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)

    # Special methods:
    def __unicode__(self):
        return self.__str__()

    def __str__(self):
        return "{s.value:.1f} kg for {s.person} at {s.when}".format(s=self)
