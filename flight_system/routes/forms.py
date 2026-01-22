# forms.py

from django import forms
from .models import Route, Airport

class RouteForm(forms.ModelForm):
    """
    Form for creating airport routes with validation.
    """
    class Meta:
        model = Route
        fields = ['from_airport', 'to_airport', 'direction', 'duration']
        widgets = {
            'from_airport': forms.Select(attrs={'class': 'form-control'}),
            'to_airport': forms.Select(attrs={'class': 'form-control'}),
            'direction': forms.Select(attrs={'class': 'form-control'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
        }
        labels = {
            'from_airport': 'From Airport Code',
            'to_airport': 'To Airport Code',
            'direction': 'Direction (Left/Right)',
            'duration': 'Duration (minutes)',
        }
    
    def clean(self):
        """
        Validate that from_airport and to_airport are different.
        """
        cleaned_data = super().clean()
        from_airport = cleaned_data.get('from_airport')
        to_airport = cleaned_data.get('to_airport')
        
        if from_airport and to_airport and from_airport == to_airport:
            raise forms.ValidationError(
                "From Airport and To Airport must be different."
            )
        
        return cleaned_data


class SearchNthNodeForm(forms.Form):
    """
    Form for searching the Nth left or right node from an airport.
    """
    airport = forms.ModelChoiceField(
        queryset=Airport.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Airport Code'
    )
    direction = forms.ChoiceField(
        choices=[('left', 'Left'), ('right', 'Right')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Direction'
    )
    n = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
        label='N (Position Number)'
    )


class LongestRouteForm(forms.Form):
    """
    Form for finding the longest route from an airport.
    """
    airport = forms.ModelChoiceField(
        queryset=Airport.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Airport Code'
    )


class ShortestRouteBetweenForm(forms.Form):
    """
    Form for finding the shortest route between two airports.
    """
    from_airport = forms.ModelChoiceField(
        queryset=Airport.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='From Airport'
    )
    to_airport = forms.ModelChoiceField(
        queryset=Airport.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='To Airport'
    )
    
    def clean(self):
        """
        Validate that airports are different.
        """
        cleaned_data = super().clean()
        from_airport = cleaned_data.get('from_airport')
        to_airport = cleaned_data.get('to_airport')
        
        if from_airport and to_airport and from_airport == to_airport:
            raise forms.ValidationError(
                "From Airport and To Airport must be different."
            )
        
        return cleaned_data