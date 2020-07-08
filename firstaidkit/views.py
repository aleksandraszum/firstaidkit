from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .forms import LoginForm, SignUpForm, BuyMedicamentForm
from django.contrib.auth import authenticate, login, logout
from datetime import date

from .models import Medicament


def index(request):
    if request.user.is_authenticated:
        return render(request, 'firstaidkit/indexpage.html')
    else:
        return render(request, 'firstaidkit/homepage.html')


# registration
def signup_view(request):
    form = SignUpForm(request.POST)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=raw_password)
        # login(request, user)
        comunicate = "Zarejestrowałeś się pomyślnie"
        return render(request, 'firstaidkit/successfulregistration.html', {'comunicate': comunicate, 'name': username})
    return render(request, 'firstaidkit/signup.html', {'form': form})


# login
def login_view(request):
    if request.user.is_authenticated:
        return render(request, 'firstaidkit/indexpage.html')
    else:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                u = form.cleaned_data['username']
                p = form.cleaned_data['password']
                user = authenticate(username=u, password=p)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        return render(request, 'firstaidkit/indexpage.html', {'form': form})
                    else:
                        communicate = "Konto zostało wyłączone."
                        return render(request, 'firstaidkit/login.html', {'form': form, 'communicate': communicate})
                else:
                    communicate = "Login bądź hasło było niepoprawne."
                    return render(request, 'firstaidkit/login.html', {'form': form, 'communicate': communicate})
        else:
            form = LoginForm()
            return render(request, 'firstaidkit/login.html', {'form': form})


# logout
def logout_view(request):
    logout(request)
    communicate = "Wylogowano pomyślnie!"
    return render(request, 'firstaidkit/homepage.html', {'communicate': communicate})


def profile(request, username):
    if request.user.is_authenticated:
        return render(request, 'firstaidkit/profile.html', {'username': username})
    else:
        return render(request, 'firstaidkit/homepage.html')


def display(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        medicaments = Medicament.objects.filter(firstaidkit=user_id)
        return render(request, 'firstaidkit/display.html', {'medicaments': medicaments})
    else:
        return render(request, 'firstaidkit/homepage.html')


def buy(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = BuyMedicamentForm(request.POST)
            if form.is_valid():
                firstaidkit_id = request.user.id
                name = str(form['name'].value())
                number_of_tablets_or_ml = int(form['number_of_tablets_or_ml'].value())
                expiration_date = form['expiration_date'].value()
                medicament = Medicament(firstaidkit_id=firstaidkit_id, name=name,
                                        number_of_tablets_or_ml=number_of_tablets_or_ml,
                                        expiration_date=expiration_date)
                medicament.save()
            return render(request, 'firstaidkit/buysuccessful.html', {"name": name})
        form = BuyMedicamentForm()
        return render(request, 'firstaidkit/buy.html', {'form': form})
    else:
        return render(request, 'firstaidkit/homepage.html')


def use(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        #medicaments = Medicament.objects.filter(firstaidkit=user_id).filter(expiration_date > date.today())

        return render(request, 'firstaidkit/use.html')
    else:
        return render(request, 'firstaidkit/homepage.html')
