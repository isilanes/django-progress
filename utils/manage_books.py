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
from books.models import Author, Book, BookStartEvent, BookEndEvent, PageUpdateEvent


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
                        default="books.json")

    parser.add_argument("--authors",
                        help="Import/export only authors. Default: import/export all.",
                        action="store_true",
                        default=False)

    parser.add_argument("--books",
                        help="Import/export only books. Default: import/export all.",
                        action="store_true",
                        default=False)

    parser.add_argument("--events",
                        help="Import/export only events. Default: import/export all.",
                        action="store_true",
                        default=False)

    return parser.parse_args(args)


def export_authors():
    author_json = {}
    for author in Author.objects.all():
        msg = f"Exporting [AUTHOR] {author}"
        print(msg)
        author_json[author.id] = {
            "name": author.name
        }

    return author_json


def export_books():
    book_dict = {}
    for book in Book.objects.all():
        msg = f"Exporting [BOOK] {book}"
        print(msg)
        book_dict[book.id] = {
            "author_pks": [author.id for author in book.authors.all()],
            "title": book.title,
            "pages": book.pages,
            "year": book.year,
        }

    return book_dict


def export_book_start_events():
    event_dict = {}
    for event in BookStartEvent.objects.all():
        msg = f"Exporting [EVENT] {event}"
        print(msg)
        event_dict[event.id] = {
            "book_pk": event.book.pk,
            "when": event.when.strftime("%Y-%m-%d %H:%M:%S"),
        }

    return event_dict


def export_page_update_events():
    event_dict = {}
    for event in PageUpdateEvent.objects.all():
        msg = f"Exporting [EVENT] {event}"
        print(msg)
        event_dict[event.id] = {
            "book_pk": event.book.pk,
            "when": event.when.strftime("%Y-%m-%d %H:%M:%S"),
            "pages_read": event.pages_read,
        }

    return event_dict


def export_book_end_events():
    event_dict = {}
    for event in BookEndEvent.objects.all():
        msg = f"Exporting [EVENT] {event}"
        print(msg)
        event_dict[event.id] = {
            "book_pk": event.book.pk,
            "when": event.when.strftime("%Y-%m-%d %H:%M:%S"),
        }

    return event_dict


def import_authors(all_data, options):
    """"Import authors from JSON data."""

    for k, val in all_data["authors"].items():
        # If already there, overwrite:
        try:
            author = Author.objects.get(pk=k)
        except ObjectDoesNotExist:
            author = Author(pk=k)

        author.name = val["name"]

        msg = f"Imported [AUTHOR] {author}"
        print(msg)

        if not options.dry_run:
            author.save()


def import_books(all_data, options):
    """Import books from JSON data."""

    for k, val in all_data["books"].items():
        # If already there, overwrite:
        try:
            book = Book.objects.get(pk=k)
        except ObjectDoesNotExist:
            book = Book(pk=k)
            book.save()

        try:
            book.authors.add(*[Author.objects.get(pk=pk) for pk in val.get("author_pks", [])])
        except ObjectDoesNotExist:
            pass
        book.title = val["title"]
        book.pages = val["pages"]
        book.year = val["year"]

        msg = f"Imported [BOOK] {book}"
        print(msg)

        if not options.dry_run:
            book.save()


def import_book_start_events(all_data, options):
    """Import book start event data from JSON data."""

    for k, val in all_data["start_events"].items():
        # If already there, overwrite:
        try:
            event = BookStartEvent.objects.get(pk=k)
        except ObjectDoesNotExist:
            event = BookStartEvent(pk=k)

        event.book = Book.objects.get(pk=val["book_pk"])
        event.when = datetime.strptime(val["when"], "%Y-%m-%d %H:%M:%S").astimezone(pytz.timezone("Europe/Madrid"))

        msg = f"Imported [EVENT] {event}"
        print(msg)

        if not options.dry_run:
            event.save()


def import_page_update_events(all_data, options):
    """Import page update events from JSON data."""

    for k, val in all_data["update_events"].items():
        # If already there, overwrite:
        try:
            event = PageUpdateEvent.objects.get(pk=k)
        except ObjectDoesNotExist:
            event = PageUpdateEvent(pk=k)
        event.book = Book.objects.get(pk=val["book_pk"])
        event.when = datetime.strptime(val["when"], "%Y-%m-%d %H:%M:%S").astimezone(pytz.timezone("Europe/Madrid"))
        event.pages_read = val["pages_read"]

        msg = f"Imported [EVENT] {event}"
        print(msg)

        if not options.dry_run:
            event.save()


def import_book_end_events(all_data, options):
    """Import book end events from JSON data."""

    for k, val in all_data["end_events"].items():
        # If already there, overwrite:
        try:
            event = BookEndEvent.objects.get(pk=k)
        except ObjectDoesNotExist:
            event = BookEndEvent(pk=k)
        event.book = Book.objects.get(pk=val["book_pk"])
        event.when = datetime.strptime(val["when"], "%Y-%m-%d %H:%M:%S").astimezone(pytz.timezone("Europe/Madrid"))

        msg = f"Imported [EVENT] {event}"
        print(msg)

        if not options.dry_run:
            event.save()


# Main:
if __name__ == "__main__":
    opts = parse_args()

    if opts.dump:
        data = {}

        # Export all, or only specified tables:
        export_all = True
        if opts.authors or opts.books or opts.events:
            export_all = False

        if opts.authors or export_all:
            data["authors"] = export_authors()

        if opts.books or export_all:
            data["books"] = export_books()

        if opts.events or export_all:
            data["start_events"] = export_book_start_events()
            data["update_events"] = export_page_update_events()
            data["end_events"] = export_book_end_events()

        # Save to file:
        with open(opts.fn, "w") as f:
            json.dump(data, f)

    elif opts.load:
        # Read from file:
        with open(opts.fn) as f:
            data = json.load(f)

        # Import all, or only specified tables:
        import_all = True
        if opts.authors or opts.books or opts.events:
            import_all = False

        if opts.authors or import_all:
            import_authors(data, opts)

        if opts.books or import_all:
            import_books(data, opts)

        if opts.events or import_all:
            import_book_start_events(data, opts)
            import_page_update_events(data, opts)
            import_book_end_events(data, opts)
