# Standard libs:
import os
import sys
import json
import django

# Python stuff:
sys.path.append("..")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DjangoProgress.settings")
django.setup()

# Our libs:
from pesos.models import Person, TimeInstant, Weight


# Functions:
def homed(file_name):
    return os.path.join(os.environ.get("HOME"), file_name)


def exported_persons():
    persons = {}
    for person in Person.objects.all():
        msg = f"Exporting [PERSON] {person}"
        print(msg)
        persons[person.id] = {
            "name": person.name
        }

    return persons


def exported_time_instants():
    instants = {}
    for instant in TimeInstant.objects.all():
        msg = f"Exporting [INSTANT] {instant}"
        print(msg)
        instants[instant.id] = {
            "timestamp": instant.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        }

    return instants


def exported_weights():
    weights = {}
    for weight in Weight.objects.all():
        msg = f"Exporting [WEIGHT] {weight}"
        print(msg)

        weights[weight.id] = {
            "value": weight.value,
            "person_pk": weight.person.pk,
            "instant_pk": weight.when.pk,
        }

    return weights


# Main:
if __name__ == "__main__":
    data = {
        "persons": exported_persons(),
        "instants": exported_time_instants(),
        "weights": exported_weights(),
    }
