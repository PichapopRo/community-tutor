from django import forms
from .models import Session

class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ['category', 'session_date_time', 'start_date', 'end_date', 'location']

        widgets = {
            'session_date_time': forms.DateInput(attrs={'type': 'date', 'class': 'flatpickr'}),
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'flatpickr'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'flatpickr'}),
        }
