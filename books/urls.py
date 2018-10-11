# Django libs:
from django.urls import path

# Our libs:
from books import views


# Constants:
app_name = "books"


# URL patterns:
urlpatterns = [
    # Main:
    path('', views.index, name="index"),

    # Misc:
    path('stats/<int:year>', views.stats, name="stats"),

    # Details:
    path('book/<int:book_id>', views.book_detail, name='book_detail'),
    path('author/<int:author_id>', views.author_detail, name='author_detail'),
]
