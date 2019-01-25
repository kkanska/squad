from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

class GenerateRandomMatchesForm(forms.Form):
    total = forms.IntegerField()