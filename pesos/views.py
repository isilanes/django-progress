# Standard libs:
import subprocess as sp
from datetime import datetime

# Django libs:
from django.utils import timezone
from django.shortcuts import render, redirect

# Our libs:
from pesos.forms import WeightForm
from pesos.models import Person, TimeInstant, Weight


# Globals:
CARBON_HOST = "localhost"
CARBON_PORT = 2003


# Index views:
def index(request):
    """Show index."""

    if request.method == "POST":
        form = WeightForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            # Create TimeInstant entry:
            ti = TimeInstant()
            ts = datetime.strptime(data["timestamp"], "%Y-%m-%d")
            current_tz = timezone.get_current_timezone()
            ti.timestamp = current_tz.localize(ts)
            h = datetime.now().hour
            m = datetime.now().minute
            ti.timestamp = ti.timestamp.replace(hour=h, minute=m)
            ti.save()

            # Create Amount entries:
            for field, value in data.items():
                if field == "timestamp":
                    continue

                try:
                    value = float(value)
                except:
                    continue

                amount = Weight()
                amount.value = value
                amount.person = Person.objects.get(name=field)
                amount.when = ti
                amount.save()

                # Send data to graphite:
                send_to_graphite(amount)

        # Back to stats_vs_time:
        return redirect("pesos:index")

    else:
        timestamp = datetime.now().strftime("%Y-%m-%d")
        initial = {
            "timestamp": timestamp,
        }

        context = {
            "form": WeightForm(initial=initial),
            "person_list": [p for p in Person.objects.all()],
        }

        return render(request, 'pesos/index.html', context)


# Helper functions:
def send_to_graphite(amount):
    """Save 'amount' info to graphite server."""

    t = amount.when.timestamp.strftime("%s")
    msg = "webprogress.pesos.{a.person.graphite_name}.kg {a.value} {t}".format(t=t, a=amount)
    cmd = "echo '{m}' | nc -q0 {h} {p}".format(m=msg, h=CARBON_HOST, p=CARBON_PORT)
    proc = sp.Popen(cmd, shell=True)
    proc.communicate()
