from django import forms
from django_flatpickr.widgets import DatePickerInput, DateTimePickerInput
from .models import Session

class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ['category', 'start_date', 'end_date', 'location', 'session_description']

        widgets = {
            'start_date': DateTimePickerInput(attrs={'class': 'flatpickr'}),
            'end_date': DateTimePickerInput(attrs={'class': 'flatpickr'}),
        }
