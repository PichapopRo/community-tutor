from django import forms
from django.contrib.auth.models import User
from django_flatpickr.widgets import DatePickerInput, DateTimePickerInput
from .models import Session, UserInfo


class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ['category', 'session_name', 'start_date', 'end_date', 'location',
                  'session_description', 'maximum_participant', 'fee']

        widgets = {
            'start_date': DateTimePickerInput(attrs={'class': 'flatpickr'}),
            'end_date': DateTimePickerInput(attrs={'class': 'flatpickr'}),
        }
        


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'class': 'datepicker'}), label="Date of Birth")


    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")
        return cleaned_data


class UserInfoForm(forms.ModelForm):
    street_address = forms.CharField(max_length=255, widget=forms.TextInput(
        attrs={'placeholder': 'Street Address'}))
    sub_district = forms.CharField(max_length=100,
                                   widget=forms.TextInput(attrs={'placeholder': 'Sub District'}))
    district = forms.CharField(max_length=100,
                               widget=forms.TextInput(attrs={'placeholder': 'District'}))
    province = forms.CharField(max_length=100,
                               widget=forms.TextInput(attrs={'placeholder': 'Province'}))
    zip_code = forms.CharField(max_length=10,
                               widget=forms.TextInput(attrs={'placeholder': 'Zip Code'}))
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'class': 'datepicker'}))
    class Meta:
        model = UserInfo
        fields = ['phone_number', 'date_of_birth']
