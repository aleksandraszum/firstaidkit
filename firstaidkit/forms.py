import datetime
from urllib import request

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import DateInput

from firstaidkit.models import Medicament


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


class UseMedicamentForm(forms.Form):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(UseMedicamentForm, self).__init__(*args, **kwargs)
        self.fields['medicament_id'] = forms.ModelChoiceField(
            queryset=Medicament.objects.order_by('name').filter(firstaidkit=user).exclude(
                expiration_date__lt=datetime.date.today()),empty_label=None)
        self.fields['number_of_tablets_or_ml'] = forms.IntegerField(label="Ilość (w sztukach bądź ml):", min_value=1,
                                                                    max_value=3)


class UtylizeMedicamentForm(forms.Form):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(UtylizeMedicamentForm, self).__init__(*args, **kwargs)
        self.fields['medicament_id'] = forms.ModelChoiceField(
            queryset=Medicament.objects.filter(firstaidkit=user).exclude(expiration_date__gt=datetime.date.today()))
