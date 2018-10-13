# Django libs:
from django import forms

# Our libs:
from pesos.models import Person


# Classes:
class WeightForm(forms.Form):
    timestamp = forms.CharField(label="Date", max_length=10)

    # Constructor:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for person in Person.objects.all():
            self.fields[person.name] = forms.FloatField(label=person.name, required=False)

