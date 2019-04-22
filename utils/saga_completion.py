# Standard libs:
import os
import sys
import django
import pylatex

# Python stuff:
sys.path.append(".")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DjangoProgress.settings")
django.setup()

# Our libs:
from books.models import Saga


# Functions:
def main():
    doc = pylatex.Document("basic")

    for saga in Saga.objects.order_by("name"):
        with doc.create(pylatex.Section(saga.name)):
            with doc.create(pylatex.Enumerate()) as elements:
                for book in saga.books:
                    color = "red"
                    if book.owned:
                        color = "blue"
                    txt = pylatex.TextColor(color, book.title)
                    elements.add_item(txt)

    doc.generate_pdf("saga_completion", clean_tex=True)


# Main:
if __name__ == "__main__":
    main()
