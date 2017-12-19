# Standard libs:
from datetime import datetime

# Django libs:
from django.http import JsonResponse
from django.shortcuts import render, redirect

# Our libs:
from gasolina.forms import VsTimeForm
from gasolina.models import PlotState, VariableConfig

# Indices:
def index(request):
    """Show stats historically."""

    if request.method == "POST":
        form = VsTimeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            # Create Stats object:
            ps = PlotState()
            ps.timestamp = datetime.strptime(data["timestamp"], "%Y-%m-%d")
            ps.timestamp = ps.timestamp.replace(hour=12)
            ps.total_kms = data["total_kms"]
            ps.partial_kms = data["partial_kms"]
            ps.litres = data["litres"]
            ps.price = data["price"]
            ps.save()

        # Back to stats_vs_time:
        return redirect("gasolina:index")

    else:
        if PlotState.objects.all():
            ps = PlotState.objects.order_by("-timestamp")[0]
            initial = {
                "timestamp": datetime.now().strftime("%Y-%m-%d"),
                "total_kms": ps.total_kms,
                "partial_kms": ps.partial_kms,
                "litres": ps.litres,
                "price": ps.price
            }
            timestamp = ps.timestamp
        else:
            initial = {}
            timestamp = datetime.utcnow()

        context = {
            "form": VsTimeForm(initial=initial),
            "timestamp": timestamp,
            "item": "intake",
        }

        return render(request, 'gasolina/stats_vs_time.html', context)


# Plots:
def plot_item(request, item):
    """Plot a single item history."""

    context = {
        "item": item,
    }
    
    return render(request, 'gasolina/plot_item.html'.format(i=item), context)


# Data URLs:
def item_data(request, item):
    """Return JSON with intake data to be plotted."""

    color_of = {
        "intake": "#cc0000",
        "range": "#00cc00",
        "kms_per_year": "#00cccc",
        "euros_per_month": "#cc0000",
    }

    data = {
        "data": data_to_plot(item),
        "color": color_of[item],
        "label": item,
        "xlabel": "mierder",
    }

    return JsonResponse(data)


# Utility functions:
def data_to_plot(item):
    """Return dictionary with data corresponding to 'item'."""
    
    data_objects = PlotState.objects.order_by("timestamp")

    # Choose data:
    if item == "intake":
        x_axis = [d.total_kms for d in data_objects[1:]]
        y_axis = [100*d.litres/d.partial_kms for d in data_objects[1:]]

    elif item == "range":
        y_axis = [d.partial_kms for d in data_objects[1:]]
        x_axis = range(len(y_axis))

    elif item == "kms_per_year":
        date0 = data_objects[0].timestamp
        days = [(d.timestamp - date0).total_seconds()/86400. for d in data_objects[1:]] # days
        x_axis = [d.timestamp.strftime("%Y-%m-%d") for d in data_objects[1:]]
        y_axis = [365*d.total_kms/dt for d, dt in zip(data_objects[1:], days)]

    elif item == "euros_per_month":
        date0 = data_objects[0].timestamp
        x_axis = [d.timestamp.strftime("%Y-%m-%d") for d in data_objects[1:]]

        y_axis = []
        gastado = 0
        for datum in data_objects[1:]:
            gastado += datum.litres * datum.price # euros gastados repostando
            epm = 30*86400*gastado/(datum.timestamp - date0).total_seconds()
            y_axis.append(epm)

    # Build data object:
    data_dict = [{"x": x, "y": y} for x, y in zip(x_axis, y_axis)]

    return data_dict

