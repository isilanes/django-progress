# Standard libs:
from datetime import datetime

# Our libs:
from .models import Book, BookEndEvent


# Functions:
def books_and_pages_so_far(year):
    """Number of books and pages read during year."""

    books_this_year = 0
    pages_this_year = 0

    for book in Book.objects.all():

        # Add 1 full book for each time book has been read this year:
        for end in BookEndEvent.objects.filter(book=book):
            if end.when.year == year:
                books_this_year += 1
                pages_this_year += book.pages

        # Add fraction of pages read, if currently reading:
        if book.is_currently_being_read:
            books_this_year += book.pages_read / book.pages
            pages_this_year += book.pages_read

    return books_this_year, pages_this_year


def days_so_far(year):
    """Total days of year, or days so far if current year."""

    now = datetime.now()
    first_day = datetime(year, 1, 1)

    if year == now.year:
        return (now - first_day).days
    else:
        last_day = datetime(year+1, 1, 1)
        return (last_day - first_day).days


# Classes:
class State(object):
    """Encapsulate all State stuff."""

    # Class variables:
    GOAL = 50  # how many books I want to read, per year

    # Constructor:
    def __init__(self, year):
        self.year = year

        # Helpers for properties:
        self._books_read = None
        self._pages_read = None

    # Public properties:
    @property
    def pages_per_book(self):
        try:
            return self.pages_read / self.books_read
        except ZeroDivisionError:
            return 0

    @property
    def pages_read(self):
        """How many pages read this year."""

        if not self._pages_read:
            self._books_read, self._pages_read = self._books_and_pages_so_far()

        return self._pages_read

    @property
    def books_read(self):
        """How many books read this year."""

        if not self._books_read:
            self._books_read, self._pages_read = self._books_and_pages_so_far()

        return self._books_read

    @property
    def pages_per_day(self):
        return self.pages_read / self._days_so_far

    @property
    def books_per_week(self):
        return 7 * self.books_per_day

    @property
    def books_per_day(self):
        return self.books_read / self._days_so_far

    @property
    def required_books(self):
        """How many books left to read this year."""

        return self.GOAL - self.books_read

    @property
    def required_pages_per_day(self):
        """How many pages we have to read, per day, for the rest of the year."""

        return self.pages_per_book * self._required_books_per_day

    @property
    def required_books_per_week(self):
        return 7 * self._required_books_per_day

    # Private methods:
    def _books_and_pages_so_far(self):
        """Number of books and pages read during year."""

        books_this_year = 0
        pages_this_year = 0

        for book in Book.objects.all():

            # Add 1 full book for each time book has been read this year:
            for end in BookEndEvent.objects.filter(book=book):
                if end.when.year == self.year:
                    books_this_year += 1
                    pages_this_year += book.pages

            # Add fraction of pages read, if currently reading:
            if book.is_currently_being_read:
                books_this_year += book.pages_read / book.pages
                pages_this_year += book.pages_read

        return books_this_year, pages_this_year

    # Private properties:
    @property
    def _days_so_far(self):
        """Total days of year, or days so far if current year."""

        now = datetime.now()
        first_day = datetime(self.year, 1, 1)

        if self.year == now.year:
            return (now - first_day).days
        else:
            last_day = datetime(self.year+1, 1, 1)
            return (last_day - first_day).days

    @property
    def _required_books_per_day(self):
        """Books/day we need to read for the remainder of the year."""

        return self.required_books / self._remaining_days

    @property
    def _remaining_days(self):
        """How many days left in year, or 1 if past year."""

        now = datetime.now()
        last_day = datetime(self.year+1, 1, 1)

        rem = 0
        if self.year == now.year:
            rem = (last_day - now).days

        if rem < 1:
            rem = 1

        return rem

