from . import forms
from django import forms
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from .models import Usuario
from .decorators import rol_requerido

from django.http import HttpResponseRedirect
from django.urls import reverse

from blessedApp.models import *
from blessedApp.forms import *
from .forms import RolForm

def login(request):
    if request.method == 'POST':
        nombre_usuario = request.POST.get('usuario')
        password = request.POST.get('password')

        try:
            usuario = Usuario.objects.get(usuario=nombre_usuario)
        except Usuario.DoesNotExist:
            messages.error(request, "Nombre de usuario o contraseña incorrectos.")
            return redirect('login')

        # Comparación  de contraseñas
        if check_password(password, usuario.password):
            # Guardar datos de sesión
            request.session['usuario_id'] = usuario.id
            request.session['usuario_nombre'] = usuario.usuario
            request.session['rol'] = usuario.rol.rol

            # Redirección según rol
            if usuario.rol.rol.lower() == 'administrador':
                return redirect('panel_admin')
            elif usuario.rol.rol.lower() == 'barbero':
                return redirect('panel_barbero')
            else:
                return redirect('panel_cliente')
        else:
            messages.error(request, "Nombre de usuario o contraseña incorrectos.")
            return redirect('login')

    return render(request, 'registration/login.html')


@rol_requerido(['Administrador'])
def panel_admin(request):
    return render(request, 'panel_admin.html')

@rol_requerido(['Barbero'])
def panel_barbero(request):
    return render(request, 'panel_barbero.html')

@rol_requerido(['Cliente'])
def panel_cliente(request):
    return render(request, 'panel_cliente.html')



def mostrarRoles(request):
    roles = Rol.objects.all()
    data = {
        'roles': roles,
        'titulo': 'Roles Disponibles'
    }
    return render (request, 'blessedApp/ver_roles.html',data)



def crearRol(request):
    formRol = RolForm()

    if request.method == 'POST':
        formRol = RolForm(request.POST)
        if formRol.is_valid():
            print("Formulario válido")
            formRol.save()
            return HttpResponseRedirect(reverse('verRoles'))
    data = {
            'formRol': formRol,
            'titulo': 'Crear Rol'
        }
    return render(request, 'blessedApp/crear_roles.html', data)
    
def editarRol(request, id):
    rol = Rol.objects.get(id=id)
    formRol = RolForm(instance=rol)
    if (request.method == 'POST'):
        formRol = RolForm(request.POST, instance=rol)
        if formRol.is_valid():
            print("Formulario válido")
            formRol.save()
            return HttpResponseRedirect(reverse('verRoles'))
        else:
            print("Formulario inválido", formRol.errors)
    data = {
        'formRol': formRol,
        'titulo': 'Editar Rol'
    }
    return render(request, 'blessedApp/crear_roles.html', data)

def eliminarRol(request, id):
    rol = Rol.objects.get(id=id)
    rol.delete()
    return HttpResponseRedirect(reverse('verRoles'))
            
