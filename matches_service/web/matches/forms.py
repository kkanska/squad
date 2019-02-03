from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
import re

from django.contrib.gis import forms as gis_forms

class MyGeoForm(gis_forms.Form):
    point = gis_forms.PointField(widget=
        gis_forms.OSMWidget(attrs={'map_width': 800, 'map_height': 500}))


class GenerateRandomMatchesForm(forms.Form):
    playground_latitude = forms.FloatField(min_value=-90.0, max_value=90.0)
    playground_longitude = forms.FloatField(min_value=-180.0, max_value=180.0)
    author_id = forms.IntegerField()
    playing_from_hour = forms.IntegerField(min_value=0, max_value=24, initial=1)
    playing_to_hour = forms.IntegerField(min_value=0, max_value=24, initial=2)
    one_match_length_in_minutes = forms.IntegerField(min_value=1, initial=20)
    playing_from_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    playing_to_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    players = forms.CharField(initial='1 2 3 4 5 6')
    discipline = forms.ChoiceField(
        choices=((0, 'football'), (1, 'basketball')),
        required=True
    )

    def clean(self):
        start_hour = self.cleaned_data['playing_from_hour']
        end_hour = self.cleaned_data['playing_to_hour']
        match_length = self.cleaned_data['one_match_length_in_minutes']
        if start_hour >= end_hour:
            msg = u"End hour should be greater than start hour!"
            self._errors["playing_to_hour"] = self.error_class([msg])
        elif match_length > (end_hour - start_hour)*60:
            msg = u"Match length is too big to fit between start and end playing hours!"
            self._errors["one_match_length_in_minutes"] = self.error_class([msg])
        start_date = self.cleaned_data['playing_from_date']
        end_date = self.cleaned_data['playing_to_date']
        if start_date > end_date:
            msg = u"End date should be greater or equal to start date!"
            self._errors["playing_to_date"] = self.error_class([msg])
        players = self.cleaned_data['players']
        if players.replace(',', '').replace(' ', '').isdigit() == False:
            msg = u"You should put here only id numbers, seperated by spaces or commas!"
            self._errors["players"] = self.error_class([msg])
