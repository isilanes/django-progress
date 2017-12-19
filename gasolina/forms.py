from django import forms

class VsTimeForm(forms.Form):
    timestamp = forms.CharField(label="Date", max_length=10)
    total_kms = forms.IntegerField(label="Total kms")
    partial_kms = forms.FloatField(label="Partial kms")
    litres = forms.FloatField(label="Litres consumed")
    price = forms.FloatField(label="Price (eur/L)")

