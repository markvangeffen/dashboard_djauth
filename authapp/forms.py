from django.contrib.auth.models import User
from django import forms
# from .models import Profile



class UserRegistration(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Repeat Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

        def clean_password2(self):
            cd = self.cleaned_data
            if cd['password'] != cd['password2']:
                raise forms.ValidationError('Passwords don\'t match.')
            return cd['password2']


class UserEditForm(forms.ModelForm):
    
    first_name = forms.CharField(max_length=75, required=True)
    last_name = forms.CharField(max_length=75, required=True)
    email = forms.EmailField(max_length=75, required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')