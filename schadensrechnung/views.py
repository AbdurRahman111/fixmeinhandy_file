from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
import os
from django.conf import settings
from benutzer.forms import KundendatenForm
# request handler
# request -> response

def schadensrechnung(request):
    # Pull data
    # Transform data
    # send emails

    return render(request, 'schadensrechnung/home.html', {'name': 'Mosh'})


def get_handy_namen(request):
    marke = request.GET.get('selected_value')
    
    fp = open(os.path.join(settings.BASE_DIR, 'schadensrechnung/static/schadensrechnung/json/marken_namen.json'))
    marken_namen = json.load(fp)
    # print("Marke:", marke)
    modelle = marken_namen[marke]
    
    options = [{'value': '0', 'label': 'Bitte wählen Sie ein Model ...'}]
    for name in modelle:
        options.append({'value': name, 'label': name})

    return JsonResponse({'options': options})


def get_preis(request):
    schadensart = request.GET.get('selected_value')
    model = request.GET.get('model')

    print(schadensart, model)
    
    no_select_flag = 0
    sonstiges_flag = 0
    preis = -1

    if schadensart == '0':
        no_select_flag = 1
    elif schadensart == '5':
        sonstiges_flag = 1
    else:
        # print("Schadensart:", SCHADENCODE[schadensart])
        # print("Model:", model)
        fp = open(os.path.join(settings.BASE_DIR, 'schadensrechnung/static/schadensrechnung/json/preise.json'))
        preisliste = json.load(fp)
        preis = preisliste[model][SCHADENCODE[schadensart]]

    response_data = {
        'sonstiges': sonstiges_flag,
        'preis': preis,
        'no_select': no_select_flag
        }

    return JsonResponse(response_data)
    


SCHADENCODE = {
    '1': "Display & Touchscreen",
    '2': "Akku",
    '3': "Ladebuchse",
    '4': "Rueckglas"
}


def Impressum(request):
    return render(request, 'schadensrechnung/Impressum.html')

def Datenschutzerklarung(request):
    return render(request, 'schadensrechnung/Datenschutzerklarung.html')