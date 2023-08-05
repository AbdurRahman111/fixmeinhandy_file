from django.shortcuts import render, redirect
from .forms import KundendatenForm
from django.contrib import messages
from .soap_client import create_soap_client, create_shipment_request
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import datetime


def marke_model(request):
    if request.method == "POST":
        marke = request.POST.get('marke')
        model = request.POST.get('model')
        art = request.POST.get('art')
        preis_input = request.POST.get('preis_input')

        if art == '1':
            main_art = 'Display & Touchscreen'
        elif art == '2':
            main_art = 'Akku'
        elif art == '3':
            main_art = 'Ladebuchse'
        elif art == '4':
            main_art = 'Rückglas'
        else:
            main_art = 'Sonstiges'

        print(marke, model, main_art)
        form = KundendatenForm()
        context = {'marke':marke, 'model':model, 'art':main_art, 'form':form, 'preis_input':preis_input}
        return render(request, 'benutzer/kundendaten.html', context)

    else:
        return redirect('/')


def terms_condition(request):
    return render(request, "benutzer/terms_condition.html")


def kundendaten_get(request):
    if request.method == 'POST':
        marke = request.POST.get('marke')
        model = request.POST.get('model')
        art = request.POST.get('art')
        preis_input = request.POST.get('preis_input')

        geburtsdatum = request.POST.get('geburtsdatum')
        date_obj = datetime.datetime.strptime(geburtsdatum, "%d/%m/%Y").date()

        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        form = KundendatenForm(request.POST)

        if form.is_valid():
            myform = form.save(commit=False)
            if request.user.is_authenticated:
                myform.User = request.user
            myform.marke = marke
            myform.model = model
            myform.Schadensart = art
            myform.kosten = preis_input
            myform.geburtsdatum = date_obj
            myform.save()


            username = form.cleaned_data.get('username')
            email = myform.email
            first_name = myform.vorname
            last_name = myform.nachname
            # print(username, email, first_name, last_name)

            if password:

                # check the error inputs

                user_username_info = User.objects.filter(username=email)
                user_email_info = User.objects.filter(email=email)

                erorr_message = ""

                if user_username_info:
                    # messages.error(request, "Username Already Exist")
                    erorr_message = "Email is Already Exist"

                elif user_email_info:
                    # messages.error(request, "Email Already Exist")
                    erorr_message = "Email is Already Exist"

                elif password != confirm_password:
                    # messages.error(request, "Passwords are not match")
                    erorr_message = "Passwords are not match!"

                elif len(password) < 8:
                    # messages.error(request, "Passwords Must be Al least 7 Digits")
                    erorr_message = "Passwords Must be Al least 8 Digits"

                if not erorr_message:
                    print('ssss')
                    print(first_name, last_name)
                    # create user
                    myuser = User.objects.create_user(email, email, password)
                    if last_name:
                        myuser.first_name = first_name
                    else:
                        myuser.first_name = ''

                    if last_name:
                        myuser.last_name = last_name
                    else:
                        myuser.last_name = ''
                    myuser.is_active = True
                    myuser.save()

                    # user = authenticate(username=email, password=password)
                    login(request, myuser)

                    if request.user.is_authenticated:
                        myform.User = request.user
                        myform.save()

                    messages.success(request,
                                     f'Your account has been created !!! you are now logged in as {first_name} {last_name}')

                    return redirect('/')

                else:
                    print('okok')
                    form = KundendatenForm()
                    value_dic = {'erorr_message': erorr_message, 'marke':marke, 'model':model, 'art':art, 'preis_input':preis_input, 'form':form}
                    return render(request, 'benutzer/kundendaten.html', value_dic)
            messages.success(request, f'Order created for {username}!')
            return redirect('/')
            # try:
            #     # Call the SOAP request function
            #     response = send_soap_request()
            #
            #     if response:
            #         # Process the SOAP response and return a JSON response
            #         # ...
            #         return JsonResponse({'result': 'success'})
            #     else:
            #         # Handle SOAP request failure
            #         # ...
            #         return JsonResponse({'result': 'error'})
            # except Exception as e:
            #     # Handle any other exceptions that might occur in the view
            #     # ...
            #     return JsonResponse({'result': 'error'})


    else:
        form = KundendatenForm()
        context = {'form':form}
        return render(request,'benutzer/kundendaten.html', context)



def kundendaten(request):
    if request.method == 'POST':
        form = KundendatenForm(request.POST)
        print(form)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('home')
    else:
        form = KundendatenForm()
    return redirect(request, 'benutzer/kundendaten.html', {'form': form})





def send_soap_request():
    try:
        soap_client = create_soap_client()
        shipment_request = create_shipment_request()

        # Replace 'ImportShipment' with the name of the operation you want to call
        response = soap_client.service.ImportShipment(shipment_request)

        # Process the SOAP response if needed
        # response_data = response['post:ResponseData']
        # ...

        return response
    except Exception as e:
        # Handle any exceptions that might occur during the SOAP request
        # ...
        return None
