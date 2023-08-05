from django import forms 
from .models import Auftrag 

class DateInput(forms.DateInput):
    input_type = 'date'

class KundendatenForm(forms.ModelForm):
    class Meta:
        model = Auftrag 
        fields = ['vorname', 
            'nachname',
            'email',
            # 'geburtsdatum',
            'telefon',
            'postleitzahl',
            'ort',
            'adresse']

        # widgets = {
        #     'geburtsdatum': DateInput()
        # }
