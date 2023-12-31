"""
URL configuration for fixmeinhandy project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from benutzer import views as benutzer_views

urlpatterns = [
    path('allgemeine_daten/', benutzer_views.kundendaten, name='dateneingabe'), #dateneingabe
    path('marke_model/', benutzer_views.marke_model, name="marke_model"),
    path('terms-and-conditions/', benutzer_views.terms_condition, name="terms_condition"),
    path('allgemeine_daten_get/', benutzer_views.kundendaten_get, name="kundendaten_get"),
    path('', include('schadensrechnung.urls'), name="home"),
    path('account/', include('account.urls')),
    path('admin/', admin.site.urls),
    re_path(r'^\.well-known/acme-challenge/(?P<path>.*)$', serve, {'document_root': '/var/www/fixmeinhandy/.well-known/acme-challenge'}),
]

