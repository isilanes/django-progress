# Django libs:
from django.urls import path

# Our libs:
from books import views


# Constants:
app_name = "books"


# URL patterns:
urlpatterns = [
    # Main:
    path('', views.stats, name="stats"),

    # Misc:
    path('index', views.index, name="index"),
    path('stats/<int:year>', views.stats, name="stats"),

    # Details:
    path('book/<int:book_id>', views.book_detail, name='book_detail'),
    path('author/<int:author_id>', views.author_detail, name='author_detail'),

    # Forms:
    path('modify_book/<int:book_id>', views.modify_book, name='modify_book'),
    path('mark_book_read/<int:book_id>', views.mark_book_read, name='mark_book_read'),
    path('add_book', views.add_book, name='add_book'),
]
