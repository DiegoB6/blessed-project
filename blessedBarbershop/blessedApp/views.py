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
            



def mostrarServicios(request):
    servicios = Servicio.objects.all()
    data = {
        'servicios': servicios,
        'titulo': 'Servicios Disponibles'
    }
    return render (request, 'blessedApp/ver_servicios.html',data)


def crearServicio(request):
    servicioForm = ServicioForm()

    if request.method == 'POST':
        servicioForm = ServicioForm(request.POST)
        if servicioForm.is_valid():
            print("Formulario válido")
            servicioForm.save()
            return HttpResponseRedirect(reverse('verServicios'))
    data = {
            'servicioForm': servicioForm,
            'titulo': 'Crear Servicio'
        }
    return render(request, 'blessedApp/crear_servicios.html', data)

def editarServicio(request, id):
    servicio = Servicio.objects.get(id=id)
    servicioForm = ServicioForm(instance=servicio)
    if (request.method == 'POST'):
        servicioForm = ServicioForm(request.POST, instance=servicio)
        if servicioForm.is_valid():
            print("Formulario válido")
            servicioForm.save()
            return HttpResponseRedirect(reverse('verServicios'))
        else:
            print("Formulario inválido", servicioForm.errors)
    data = {
        'servicioForm': servicioForm,
        'titulo': 'Editar Servicio'
    }
    return render(request, 'blessedApp/crear_servicios.html', data)

def eliminarServicio(request, id):
    servicio = Servicio.objects.get(id=id)
    servicio.delete()
    return HttpResponseRedirect(reverse('verServicios'))



def mostrarUsuarios(request):
    usuarios = Usuario.objects.all()
    data = {
        'usuarios': usuarios,
        'titulo': 'Usuarios Disponibles'
    }
    return render (request, 'blessedApp/ver_usuarios.html',data)


def crearUsuario(request):
    usuarioForm = UsuarioForm()

    if request.method == 'POST':
        usuarioForm = UsuarioForm(request.POST)
        if usuarioForm.is_valid():
            print("Formulario válido")
            usuarioForm.save()
            return HttpResponseRedirect(reverse('verUsuarios'))
    data = {
            'usuarioForm': usuarioForm,
            'titulo': 'Crear Usuario'
        }
    return render(request, 'blessedApp/crear_usuarios.html', data)

def editarUsuario(request, id):
    usuario = Usuario.objects.get(id=id)
    usuarioForm = UsuarioForm(instance=usuario) 
    if (request.method == 'POST'):
        usuarioForm = UsuarioForm(request.POST, instance=usuario)
        if usuarioForm.is_valid():
            print("Formulario válido")
            usuarioForm.save()
            return HttpResponseRedirect(reverse('verUsuarios'))
        else:
            print("Formulario inválido", usuarioForm.errors)
    data = {
        'usuarioForm': usuarioForm,
        'titulo': 'Editar Usuario'
    }
    return render(request, 'blessedApp/crear_usuarios.html', data)


def eliminarUsuario(request, id):
    usuario = Usuario.objects.get(id=id)
    usuario.delete()
    return HttpResponseRedirect(reverse('verUsuarios'))




def mostrarDisponibilidades(request):
    disponibilidades = Disponibilidad.objects.all()
    data = {
        'disponibilidades': disponibilidades,
        'titulo': 'Disponibilidades Disponibles'
    }
    return render (request, 'blessedApp/ver_disponibilidades.html',data)

def crearDisponibilidad(request):
    disponibilidadForm = DisponibilidadForm()

    if request.method == 'POST':
        disponibilidadForm = DisponibilidadForm(request.POST)
        if disponibilidadForm.is_valid():
            print("Formulario válido")
            disponibilidadForm.save()
            return HttpResponseRedirect(reverse('verDisponibilidades'))
    data = {
            'disponibilidadForm': disponibilidadForm,
            'titulo': 'Crear Disponbilidad'
        }
    return render(request, 'blessedApp/crear_disponibilidades.html', data)

def editarDisponibilidad(request, id):
    disponibilidad = Disponibilidad.objects.get(id=id)
    disponibilidadForm = DisponibilidadForm(instance=disponibilidad) 
    if (request.method == 'POST'):
        disponibilidadForm = DisponibilidadForm(request.POST, instance=disponibilidad)
        if disponibilidadForm.is_valid():
            print("Formulario válido")
            disponibilidadForm.save()
            return HttpResponseRedirect(reverse('verDisponibilidades'))
        else:
            print("Formulario inválido", disponibilidadForm.errors)
    data = {
        'disponibilidadForm': disponibilidadForm,
        'titulo': 'Editar Disponibilidad'
    }
    return render(request, 'blessedApp/crear_disponibilidades.html', data)

def eliminarDisponibilidad(request, id):
    disponibilidad = Disponibilidad.objects.get(id=id)
    disponibilidad.delete()
    return HttpResponseRedirect(reverse('verDisponibilidades'))