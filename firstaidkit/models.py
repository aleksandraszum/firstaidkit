from datetime import datetime

from django.contrib.auth.models import User
from django.db import models


class Medicament(models.Model):
    firstaidkit = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=False)
    number_of_tablets_or_ml = models.PositiveIntegerField(default=0)
    date_of_purchase = models.DateField(default=datetime.now, blank=True)
    expiration_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.name}"


class MedicineManagement(models.Model):
    firstaidkit = models.ForeignKey(User, on_delete=models.CASCADE)
    medicament = models.CharField(max_length=100, null=False)
    number_of_tablets_or_ml = models.PositiveIntegerField(default=0)
    date_of_used = models.DateField(default=datetime.now, blank=True)
    is_used = models.BooleanField(default=False)
    is_used_absolute = models.BooleanField(default=False)
    is_utylized = models.BooleanField(default=False)
    is_buyed = models.BooleanField(default=False)

    def __str__(self):
        if self.is_used:
            return f"{self.date_of_used} - used"
        elif self.is_buyed:
            return f"{self.date_of_used} - buyed"
        elif self.is_used_absolute:
            return f"{self.date_of_used} - absolute used"
        else:
            return f"{self.date_of_used} - utylized"

