# Django libs:
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect

# Our libs:
from . import statistics
from .models import Book, Author, BookStartEvent, Saga
from .forms import BookForm, AddBookForm


# Views:
def index(request):
    """Index view."""

    context = {
        "currently_reading_books": currently_reading_books(),
        "currently_ordered_books": currently_ordered_books(),
        "already_read_books": already_read_books(),
    }

    return render(request, "books/index.html", context)


def sagas(request):
    """Saga view."""

    sagas = Saga.objects.all()
    for saga in sagas:
        print(saga)
        print(saga.book_set.all())

    context = {
        "sagas": sagas,
    }

    return render(request, "books/sagas.html", context)


def book_detail(request, book_id):
    """Detail view for a book."""

    book = Book.objects.get(pk=book_id)

    context = {
        "book": book,
     }

    return render(request, "books/book_detail.html", context)


def modify_book(request, book_id):
    """Form to modify state of book."""

    book = Book.objects.get(pk=book_id)

    if request.method == "POST":
        form = BookForm(request.POST or None)
        if form.is_valid():
            pages_read = form.cleaned_data.get("pages_read")
            if pages_read is not None:
                book.set_pages(pages_read)
                return redirect("books:book_detail", book_id=book_id)

    initial = {
        "pages_read": book.pages_read,
    }
    form = BookForm(initial=initial)

    context = {
        "form": form,
        "book": book,
    }

    return render(request, 'books/modify_book.html', context)


def add_book(request):
    """Form to add a book."""

    if request.method == "POST":
        form = AddBookForm(request.POST or None)
        if form.is_valid():
            title = form.cleaned_data.get("title")
            if title is not None:
                # Add data:
                book = Book()
                book.title = title
                book.pages = form.cleaned_data.get("pages")
                book.year = form.cleaned_data.get("year")

                if "acquired" not in request.POST and "reading" not in request.POST:
                    book.owned = False

                if "ordered" in request.POST:
                    book.ordered = True

                # Saga info:
                s = form.cleaned_data.get("saga")
                if s:
                    try:
                        book.saga = Saga.objects.get(name=s)
                    except ObjectDoesNotExist:
                        s = Saga(name=s)
                        s.save()
                        book.saga = s
                    book.index_in_saga = form.cleaned_data.get("index")
                book.save()  # we must save BEFORE we add many-to-many field items (author(s) below)

                # Add author data:
                author_names = [a.strip() for a in form.cleaned_data.get("author", "").split(",")]
                for author_name in author_names:
                    try:
                        author = Author.objects.get(name=author_name)
                    except Author.DoesNotExist:
                        author = Author(name=author_name)
                        author.save()
                    book.authors.add(author)

                # Add started reading:
                if "reading" in request.POST:
                    start = BookStartEvent()
                    start.book = book
                    start.when = timezone.now()
                    start.save()

                return redirect("books:book_detail", book_id=book.id)

    initial = {
        "pages": 0,
        "year": 0,
        "saga": None,
        "index": None,
    }
    form = AddBookForm(initial=initial)

    context = {
        "form": form,
    }

    return render(request, 'books/add_book.html', context)


def mark_book_read(request, book_id):
    """Come here with a POST to mark a book read."""

    if request.method == "POST":
        book = Book.objects.get(pk=book_id)
        book.mark_read()

    return redirect("books:book_detail", book_id=book_id)


def author_detail(request, author_id=None):
    """Detail view for an author."""

    author = Author.objects.get(pk=author_id)

    context = {
        "author": author,
    }

    return render(request, "books/author_detail.html", context)


def stats(request, year=None):
    """View with statistics for 'year'."""

    # If no year given, use current:
    if year is None:
        year = timezone.now().year

    context = {
        "year": year,
        "state": statistics.State(year),
        "currently_reading_books": currently_reading_books(),
    }

    return render(request, "books/stats.html", context)


# Helper functions:
def currently_reading_books():
    """Return list of books currently being read, unsorted."""

    return [book for book in Book.objects.all() if book.is_currently_being_read]


def already_read_books():
    """Return list of books already read, sorted by finish date."""

    return [y for x, y in sorted([(book.date_read, book) for book in Book.objects.all()
                                  if book.is_already_read], reverse=True)]


def currently_ordered_books():
    """Return list of books currently ordered, but not yet received, unsorted."""

    return [book for book in Book.objects.all() if book.ordered]
