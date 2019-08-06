# Standard libs:
import os
import sys
import json
import pytz
import django
import argparse
from datetime import datetime

# Python stuff:
from django.core.exceptions import ObjectDoesNotExist
sys.path.append("..")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DjangoProgress.settings")
django.setup()

# Our libs:
from gasolina.models import PlotState, VariableConfig


# Functions:
def parse_args(args=sys.argv[1:]):
    parser = argparse.ArgumentParser()

    parser.add_argument("--dump",
                        help="Export DB to JSON file. Default: do nothing.",
                        action="store_true",
                        default=False)

    parser.add_argument("--load",
                        help="Import DB from JSON file. Default: do nothing.",
                        action="store_true",
                        default=False)

    parser.add_argument("--dry-run",
                        help="Fake import. Default: if asked to import, do it.",
                        action="store_true",
                        default=False)

    parser.add_argument("--fn",
                        help="Export DB to / import DB from JSON file named OUT. Default: do nothing.",
                        default="gasolina.json")

    return parser.parse_args(args)


def export_plot_state():
    """Export table PlotState."""

    ps_json = {}
    for ps in PlotState.objects.all():
        msg = f"Exporting [PlotState] {ps}"
        print(msg)
        ps_json[ps.id] = {
            "timestamp": ps.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "total_kms": ps.total_kms,
            "partial_kms": ps.partial_kms,
            "litres": ps.litres,
            "price": ps.price,
        }

    return ps_json


def export_variable_config():
    """Export table VariableConfig."""

    vc_json = {}
    for vc in VariableConfig.objects.all():
        msg = f"Exporting [VariableConfig] {vc}"
        print(msg)
        vc_json[vc.id] = {
            "name": vc.name,
            "long_name": vc.long_name,
            "style": vc.style,
            "objective": vc.objective,
        }

    return vc_json


def import_plot_state(all_data, options):
    """Import PlotState table from JSON data."""

    for k, val in all_data["plot_states"].items():
        # If already exists, overwrite. Else, create:
        try:
            ps = PlotState.objects.get(pk=k)
        except ObjectDoesNotExist:
            ps = PlotState(pk=k)

        ps.timestamp = datetime.strptime(val["timestamp"], "%Y-%m-%d %H:%M:%S").astimezone(pytz.timezone("Europe/Madrid"))
        ps.total_kms = val["total_kms"]
        ps.partial_kms = val["partial_kms"]
        ps.litres = val["litres"]
        ps.price = val["price"]

        msg = f"Imported [PlotState] {ps}"
        print(msg)

        if not options.dry_run:
            ps.save()


def import_variable_config(all_data, options):
    """Import VariableConfig table from JSON data."""

    for k, val in all_data["variable_config"].items():
        # If already exists, overwrite. Else, create:
        try:
            vc = VariableConfig.objects.get(pk=k)
        except ObjectDoesNotExist:
            vc = VariableConfig(pk=k)

        vc.name = val["name"]
        vc.long_name = val["long_name"]
        vc.style = val["style"]
        vc.objective = val["objective"]

        msg = f"Imported [VariableConfig] {vc}"
        print(msg)

        if not options.dry_run:
            vc.save()


# Main:
if __name__ == "__main__":
    opts = parse_args()

    if opts.dump:
        data = dict()

        data["plot_states"] = export_plot_state()
        data["variable_config"] = export_variable_config()

        # Save to file:
        with open(opts.fn, "w") as f:
            json.dump(data, f)

    elif opts.load:
        # Read from file:
        with open(opts.fn) as f:
            data = json.load(f)

        import_plot_state(data, opts)

