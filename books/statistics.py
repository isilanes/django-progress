# Standard libs:
from datetime import datetime

# Our libs:
from .models import Book, BookEndEvent


# Classes:
class State(object):
    """Encapsulate all State stuff."""

    # Class variables:
    GOAL = 36  # how many books I want to read, per year

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
    def expected_books_so_far(self):
        """How many books we should have read so far in the year."""

        return self.GOAL * self.year_fraction_passed

    @property
    def book_superavit_percent(self):
        """How many books ahead we are in the book count up to now in the year."""

        return 100. * (self.books_read - self.expected_books_so_far) / self.expected_books_so_far

    @property
    def book_percent_read(self):
        return 100. * self.books_read / self.GOAL

    @property
    def book_deficit_percent(self):
        return -1. * self.book_superavit_percent

    @property
    def pages_per_day(self):
        return self.pages_read / self.days_so_far

    @property
    def books_per_week(self):
        return 7 * self.books_per_day

    @property
    def books_per_day(self):
        return self.books_read / self.days_so_far

    @property
    def required_books(self):
        """How many books left to read this year."""

        return self.GOAL - self.books_read

    @property
    def required_pages_per_day(self):
        """How many pages we have to read, per day, for the rest of the year."""

        return self.pages_per_book * self.required_books_per_day

    @property
    def required_books_per_week(self):
        """Books/week we need to read for the remainder of the year."""

        return 7 * self.required_books_per_day

    @property
    def required_books_per_day(self):
        """Books/day we need to read for the remainder of the year."""

        return self.required_books / self.remaining_days

    @property
    def remaining_days(self):
        return 365 - self.days_so_far

    @property
    def year_fraction_passed(self):
        """Fraction of year already passed. 1.0 if not current year."""

        now = datetime.now()

        if self.year == now.year:
            passed_seconds = (now - datetime(self.year, 1, 1)).total_seconds()

            return passed_seconds / 31536000.  # 31536000 seconds in a year

        else:
            return 1.0

    @property
    def days_so_far(self):
        """Days so far in this year. 365 if not current year."""

        return self.year_fraction_passed * 365

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
                if book.pages == 0:
                    return 0, 0
                books_this_year += book.pages_read / book.pages
                pages_this_year += book.pages_read

        return books_this_year, pages_this_year


