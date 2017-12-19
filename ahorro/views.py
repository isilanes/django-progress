# Standard libs:
from datetime import datetime

# Django libs:
from django.http import JsonResponse
from django.shortcuts import render, redirect

# Our libs:
from ahorro.forms import AmountForm
from ahorro.models import  Amount, TimeInstant, Account

# Index views:
def index(request):
    """Show index."""

    if request.method == "POST":
        form = AmountForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            
            # Create TimeInstant entry:
            ti = TimeInstant()
            ti.timestamp = datetime.strptime(data["timestamp"], "%Y-%m-%d")
            ti.timestamp = ti.timestamp.replace(hour=12)
            ti.save()

            # Create Amount entries:
            for field, value in data.items():
                if field == "timestamp":
                    continue

                amount = Amount()
                amount.value = value
                amount.account = Account.objects.get(name=field)
                amount.when = ti
                amount.save()

        # Back to stats_vs_time:
        return redirect("ahorro:index")

    else:
        timestamp = datetime.now().strftime("%Y-%m-%d")
        initial = {
            "timestamp": timestamp,
        }
        for account in Account.objects.all():
            initial[account.name] = 0.0

        context = {
            "form": AmountForm(initial=initial),
            "account_list": [a for a in Account.objects.all()],
        }

        return render(request, 'ahorro/index.html', context)


# Plots:
def plot_item(request, item):
    """Plot a single item history."""

    context = {
        "item": item,
        "account_list": [a for a in Account.objects.all()],
    }
    
    return render(request, 'ahorro/plot_item.html'.format(i=item), context)


# Data URLs:
def data_to_plot(item):
    """Return dictionary with data corresponding to 'item'."""
    
    #data_objects = PlotState.objects.order_by("timestamp")
    x_axis,  y_axis = [], []

    # Choose data:
    if item == "total":
        time_amount = [(ti.timestamp, ti.total_amount) for ti in TimeInstant.objects.order_by("timestamp")]
        xy_axes = [(t.strftime("%Y-%m-%d %H:%M"), a) for t, a in time_amount]

    else:
        amounts = Amount.objects.filter(account__name=item).order_by("when")
        xy_axes = [(a.when.timestamp.strftime("%Y-%m-%d %H:%M"), a.value) for a in amounts]


    # Build data object:
    data_dict = [{"x": x, "y": y} for x, y in xy_axes]

    return data_dict

def item_data(request, item):
    """Return JSON with item data to be plotted."""

    if item == "total":
        color = "#00cc00"
    else:
        color = Account.objects.get(name=item).color

    data = {
        "data": data_to_plot(item),
        "color": color,
        "label": item,
    }
    
    return JsonResponse(data)

