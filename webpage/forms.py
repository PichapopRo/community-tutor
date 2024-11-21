from django import forms
from .models import Course


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['course_name', 'date']

    widgets = {
        'date': forms.DateInput(attrs={'type': 'date'}),
    }
