# Standard libs:
import os
import sys
import json
import pytz
import django
from datetime import datetime

# Python stuff:
from django.core.exceptions import ObjectDoesNotExist
sys.path.append("..")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "WebProgress.settings")
django.setup()

# Our libs:
from books.models import Author, Book, BookStartEvent, BookEndEvent, PageUpdateEvent


# Functions:
def import_authors(in_fn="authors.json"):
    with open(in_fn) as f:
        authors = json.load(f)

    for k, val in authors.items():
        # If already there, overwrite:
        try:
            author = Author.objects.get(pk=k)
        except ObjectDoesNotExist:
            author = Author(pk=k)
        author.name = val["name"]
        msg = f"Imported [AUTHOR] {author}"
        print(msg)
        author.save()


def import_books(in_fn="books.json"):
    with open(in_fn) as f:
        books = json.load(f)

    for k, val in books.items():
        # If already there, overwrite:
        try:
            book = Book.objects.get(pk=k)
        except ObjectDoesNotExist:
            book = Book(pk=k)
        book.author = Author.objects.get(pk=val["author_pk"])
        book.title = val["title"]
        book.pages = val["pages"]
        book.year = val["year"]
        msg = f"Imported [BOOK] {book}"
        print(msg)
        book.save()


def import_book_start_events(in_fn="book_start_events.json"):
    with open(in_fn) as f:
        events = json.load(f)

    for k, val in events.items():
        # If already there, overwrite:
        try:
            event = BookStartEvent.objects.get(pk=k)
        except ObjectDoesNotExist:
            event = BookStartEvent(pk=k)
        event.book = Book.objects.get(pk=val["book_pk"])
        event.when = datetime.strptime(val["when"], "%Y-%m-%d %H:%M:%S").astimezone(pytz.timezone("Europe/Madrid"))
        msg = f"Imported [EVENT] {event}"
        print(msg)
        event.save()


def import_book_end_events(in_fn="book_end_events.json"):
    with open(in_fn) as f:
        events = json.load(f)

    for k, val in events.items():
        # If already there, overwrite:
        try:
            event = BookEndEvent.objects.get(pk=k)
        except ObjectDoesNotExist:
            event = BookEndEvent(pk=k)
        event.book = Book.objects.get(pk=val["book_pk"])
        event.when = datetime.strptime(val["when"], "%Y-%m-%d %H:%M:%S").astimezone(pytz.timezone("Europe/Madrid"))
        msg = f"Imported [EVENT] {event}"
        print(msg)
        event.save()


# Main:
if __name__ == "__main__":
    import_authors()
    import_books()
    import_book_start_events()
    import_book_end_events()
