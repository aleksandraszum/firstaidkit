from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import DateInput


class LoginForm(forms.Form):
    username = forms.CharField(label='Nazwa użytkownika', max_length=64)
    password = forms.CharField(widget=forms.PasswordInput())


class SignUpForm(UserCreationForm):
    username = forms.CharField(label="Nazwa użytkownika:")
    password1 = forms.CharField(widget=forms.PasswordInput(), label="Hasło:")
    password2 = forms.CharField(widget=forms.PasswordInput(), label="Powtórz hasło:")

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class BuyMedicamentForm(forms.Form):
    name = forms.CharField(label="Nazwa leku", max_length=50)
    number_of_tablets_or_ml = forms.IntegerField(label="Ilość (w sztukach bądź ml)")
    expiration_date = forms.DateField(label="Data ważności", widget=DateInput(attrs={'type': 'date'}))
