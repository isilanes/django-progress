# Django libs:
from django.shortcuts import render

# Bokeh libs:
from bokeh.plotting import figure
from bokeh.embed import components

# Our libs:
from . import statistics
from .models import Book


# Views:
def index(request):
    """Index view."""

    context = {
        "currently_reading_books": currently_reading_books(),
        "already_read_books": already_read_books(),
    }

    return render(request, "books/index.html", context)


def book_detail(request, book_id=None):
    """Detail view for a book."""

    book = Book.objects.get(pk=book_id)
    progress_plot_script, progress_plot_div = components(mk_book_progress_plot(book))
    rate_plot_script, rate_plot_div = components(mk_page_rate_plot(book))

    context = {
        "book": book,
        "progress_plot_script": progress_plot_script,
        "progress_plot_div": progress_plot_div,
        "rate_plot_script": rate_plot_script,
        "rate_plot_div": rate_plot_div,
     }

    return render(request, "books/book_detail.html", context)


def stats(request, year):
    """View with statistics for 'year'."""

    context = {
        "year": year,
        "state": statistics.State(year)
    }

    return render(request, "books/stats.html", context)


def mk_book_progress_plot(book):
    """Generate and return Bokeh plot object for book page progress."""

    # Plot data:
    X, Y = [], []
    for event in book.events:
        x = event.when
        y = event.page_equivalent
        X.append(x)
        Y.append(y)

    # Build plot:
    plot = figure(title="Reading progress",
                  x_axis_label='Date',
                  y_axis_label='Pages read')

    plot.line(X, Y, legend='pages', line_width=2)

    return plot


def mk_page_rate_plot(book):
    """Generate and return Bokeh plot object for book page read rate."""

    # Plot data:
    X, Y = [], []
    previous_p = previous_t = None
    for event in book.events:
        x = event.when
        y = event.page_equivalent
        dy = 0
        if previous_p is not None:
            dy = 86400 * (y - previous_p) / (x - previous_t).total_seconds()

        previous_t = x
        previous_p = y

        X.append(x)
        Y.append(dy)

    # Build plot:
    plot = figure(title="Reading rate",
                  x_axis_label='Date',
                  y_axis_label='pages/day')

    plot.line(X, Y, line_width=2)

    return plot


# Helper functions
def currently_reading_books():
    """Return list of books currently being read, unsorted."""

    return [book for book in Book.objects.all() if book.is_currently_being_read]


def already_read_books():
    """Return list of books already read, sorted by finish date."""

    return [y for x, y in sorted([(book.date_read, book) for book in Book.objects.all()
                                  if book.is_already_read], reverse=True)]
