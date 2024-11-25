from django import forms
from django_flatpickr.widgets import DatePickerInput, DateTimePickerInput
from .models import Session

class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ['category', 'session_date_time', 'start_date', 'end_date', 'location']

        widgets = {
            'session_date_time': DatePickerInput(attrs={'class': 'flatpickr'}),
            'start_date': DateTimePickerInput(attrs={'class': 'flatpickr'}),
            'end_date': DateTimePickerInput(attrs={'class': 'flatpickr'}),
        }
