# Django libs:
from django import forms


# Forms:
class BookForm(forms.Form):
    pages_read = forms.IntegerField(label="Pages read", max_value=10000, required=False)


class AddBookForm(forms.Form):
    title = forms.CharField(label="Title")
    author = forms.CharField(label="Author(s)")
    pages = forms.IntegerField(label="Pages")
    year = forms.IntegerField(label="Year")
    saga = forms.CharField(label="Saga")
    index = forms.CharField(label="Index in saga")
