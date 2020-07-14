import datetime
import time

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, Context

from .forms import LoginForm, SignUpForm, BuyMedicamentForm, UseMedicamentForm, UtylizeMedicamentForm
from django.contrib.auth import authenticate, login, logout
from datetime import date

from .models import Medicament, MedicineManagement


def index(request):
    if request.user.is_authenticated:
        management = MedicineManagement.objects.filter(firstaidkit=request.user.id).order_by('-pk')[:8]
        print(management)
        return render(request, 'firstaidkit/indexpage.html', {'managements': management})
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


# display the first aid kit
def display(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        medicaments = Medicament.objects.filter(firstaidkit=user_id).order_by('expiration_date')
        return render(request, 'firstaidkit/display.html', {'medicaments': medicaments})
    else:
        return render(request, 'firstaidkit/homepage.html')


# add new medicaments
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
                management = MedicineManagement(firstaidkit_id=firstaidkit_id, medicament=name,
                                                number_of_tablets_or_ml=number_of_tablets_or_ml, is_buyed=True)
                management.save()
            return render(request, 'firstaidkit/buysuccessful.html', {"name": name})
        form = BuyMedicamentForm()
        return render(request, 'firstaidkit/buy.html', {'form': form})
    else:
        return render(request, 'firstaidkit/homepage.html')


# take medicine
def use(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = UseMedicamentForm(request.POST, user=request.user.id)
            medicament_id = int(form['medicament_id'].value())
            name = Medicament.objects.filter(pk=medicament_id).first()
            medicament_amount = int(form['number_of_tablets_or_ml'].value())
            medicament = Medicament.objects.get(pk=medicament_id)

            if medicament.number_of_tablets_or_ml >= medicament_amount:
                medicament.number_of_tablets_or_ml = medicament.number_of_tablets_or_ml - medicament_amount
                medicament.save()

                management = MedicineManagement(firstaidkit=User(pk=request.user.id), medicament=name,
                                                number_of_tablets_or_ml=medicament_amount, is_used=True)
                management.save()

                if medicament.number_of_tablets_or_ml == 0:
                    management2 = MedicineManagement(firstaidkit_id=request.user.id, medicament=medicament,
                                                    number_of_tablets_or_ml=medicament_amount,
                                                    is_used_absolute=True)
                    management2.save()
                    medicament.delete()
                    communicate = "Skończył się lek: "
                    return render(request, 'firstaidkit/successfuluse.html',
                                  {'medicament': name, 'amount': medicament_amount, 'communicate': communicate})

                return render(request, 'firstaidkit/successfuluse.html',
                              {'medicament': name, 'amount': medicament_amount})
            else:
                communicate = "Nie możesz zażyć więcej leków, niż masz w apteczce!"
                form = UseMedicamentForm(request.POST, user=request.user.id)
                return render(request, 'firstaidkit/use.html', {'form': form, 'communicate': communicate})

        form = UseMedicamentForm(request.POST, user=request.user.id)
        return render(request, 'firstaidkit/use.html', {'form': form})
    else:
        return render(request, 'firstaidkit/homepage.html')


# utylize medicaments
def utylize(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = UtylizeMedicamentForm(request.POST, user=request.user.id)
            medicament_id = int(form['medicament_id'].value())
            medicament = Medicament.objects.get(pk=medicament_id)
            name = medicament.name
            medicament_amount = medicament.number_of_tablets_or_ml
            management = MedicineManagement(firstaidkit=User(pk=request.user.id),
                                            medicament=name,
                                            number_of_tablets_or_ml=medicament_amount, is_used=False,
                                            is_utylized=True)
            management.save()
            medicament.delete()

            return render(request, 'firstaidkit/successfulutylize.html',
                          {'medicament': name})
        medicament = (Medicament.objects.filter(firstaidkit=request.user.id).exclude(
            expiration_date__gt=datetime.date.today()).values_list('number_of_tablets_or_ml'))
        if medicament.exists():
            form = UtylizeMedicamentForm(request.POST, user=request.user.id)
            return render(request, 'firstaidkit/utylize.html', {'form': form})
        else:
            return render(request, 'firstaidkit/notutylize.html')

    else:
        return render(request, 'firstaidkit/homepage.html')


