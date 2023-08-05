from django.db import models
from django.contrib.auth.models import User



class Auftrag(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True, blank=True)
    email = models.EmailField()
    vorname = models.CharField(max_length=30)
    nachname = models.CharField(max_length=30)
    geburtsdatum = models.DateField()
    postleitzahl = models.IntegerField()
    ort = models.CharField(max_length=30)
    adresse = models.CharField(max_length=50)
    handy = models.CharField(max_length=30)
    schaden = models.CharField(max_length=30)
    marke = models.CharField(max_length=30)
    model = models.CharField(max_length=30)
    Schadensart = models.CharField(max_length=30)
    kosten = models.FloatField(blank=True, null=True)
    telefon = models.CharField(max_length=20, blank=True, null=True)
