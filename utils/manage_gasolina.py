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
    """Export Table of state points."""

    ps_json = {}
    for ps in PlotState.objects.all():
        msg = f"Exporting [PlotState] {ps}"
        print(msg)
        ps_json[ps.id] = {
            "timestamp": datetime.strftime(ps.timestamp, "%Y-%m-%d %H:%M:%S"),
            "total_kms": ps.total_kms,
            "partial_kms": ps.partial_kms,
            "litres": ps.litres,
            "price": ps.price,
        }

    return ps_json


# Main:
if __name__ == "__main__":
    opts = parse_args()

    if opts.dump:
        data = dict()

        data["plot_states"] = export_plot_state()

        # Save to file:
        with open(opts.fn, "w") as f:
            json.dump(data, f)
