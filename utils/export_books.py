# Standard libs:
import os
import sys
import json
import django

# Python stuff:
sys.path.append("..")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "WebProgress.settings")
django.setup()

# Our libs:
from books.models import Author, Book, BookStartEvent, BookEndEvent, PageUpdateEvent


# Functions:
def homed(file_name):
    return os.path.join(os.environ.get("HOME"), file_name)


def export_authors(out_fn=homed("authors.json")):
    author_json = {}
    for author in Author.objects.all():
        msg = f"Exporting [AUTHOR] {author}"
        print(msg)
        author_json[author.id] = {
            "name": author.name
        }

    with open(out_fn, "w") as f:
        json.dump(author_json, f)


def export_books(out_fn=homed("books.json")):
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

    with open(out_fn, "w") as f:
        json.dump(book_dict, f)


def export_book_start_events(out_fn=homed("book_start_events.json")):
    event_dict = {}
    for event in BookStartEvent.objects.all():
        msg = f"Exporting [EVENT] {event}"
        print(msg)
        event_dict[event.id] = {
            "book_pk": event.book.pk,
            "when": event.when.strftime("%Y-%m-%d %H:%M:%S"),
        }

    with open(out_fn, "w") as f:
        json.dump(event_dict, f)


def export_page_update_events(out_fn=homed("page_update_events.json")):
    event_dict = {}
    for event in PageUpdateEvent.objects.all():
        msg = f"Exporting [EVENT] {event}"
        print(msg)
        event_dict[event.id] = {
            "book_pk": event.book.pk,
            "when": event.when.strftime("%Y-%m-%d %H:%M:%S"),
            "pages_read": event.pages_read,
        }

    with open(out_fn, "w") as f:
        json.dump(event_dict, f)


def export_book_end_events(out_fn=homed("book_end_events.json")):
    event_dict = {}
    for event in BookEndEvent.objects.all():
        msg = f"Exporting [EVENT] {event}"
        print(msg)
        event_dict[event.id] = {
            "book_pk": event.book.pk,
            "when": event.when.strftime("%Y-%m-%d %H:%M:%S"),
        }

    with open(out_fn, "w") as f:
        json.dump(event_dict, f)


# Main:
if __name__ == "__main__":
    export_authors()
    export_books()
    export_book_start_events()
    export_page_update_events()
    export_book_end_events()
