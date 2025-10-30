"""
URL configuration for blessedBarbershop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from django.views.generic.base import TemplateView
from blessedApp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',TemplateView.as_view(template_name='index.html'), name='home'), 
    path('login/', login, name='login'),
    path('panelAdmin/', panel_admin, name='panel_admin'),
    path('panelBarbero/', panel_barbero, name='panel_barbero'),
    path('panelCliente/', panel_cliente, name='panel_cliente'),

    path('verRoles/', mostrarRoles, name='verRoles'),
    path('crearRol/', crearRol, name='crearRol'),
    path('editarRol/<int:id>/', editarRol, name='editarRol'),
    path('eliminarRol/<int:id>/', eliminarRol, name='eliminarRol'),


]
