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



def mostrarReservas(request):
    reservas = Reserva.objects.all()
    data = {
        'reservas': reservas,
        'titulo': 'Reservas Disponibles'
    }
    return render (request, 'blessedApp/ver_reservas.html',data)



def crearReserva(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        messages.error(request, "Debe iniciar sesión para crear una reserva.")
        return redirect('login')

    cliente = Usuario.objects.get(id=usuario_id)

    if request.method == 'POST':
        reservaForm = ReservaForm(request.POST)
        if reservaForm.is_valid():
            reserva = reservaForm.save(commit=False)
            reserva.cliente = cliente

            # 🔹 Verificar disponibilidad del barbero en la hora seleccionada
            disponibilidad_ocupada = Disponibilidad.objects.filter(
                barbero=reserva.barbero,
                fecha=reserva.fecha,
                hora_inicio__lte=reserva.hora_inicio,
                hora_fin__gte=reserva.hora_inicio,
                disponible=False
            ).exists()

            if disponibilidad_ocupada:
                messages.error(request, "⚠️ El barbero no está disponible en el horario seleccionado.")
                # Se vuelve a mostrar el formulario sin romper el flujo
                data = {
                    'reservaForm': reservaForm,
                    'titulo': 'Crear Reserva'
                }
                return render(request, 'blessedApp/crear_reservas.html', data)

            # 🔹 Asignar estado "Pendiente" automáticamente
            estado_pendiente, _ = Estado.objects.get_or_create(estado="Pendiente")
            reserva.estado = estado_pendiente

            reserva.save()
            messages.success(request, "✅ Reserva creada exitosamente.")
            return HttpResponseRedirect(reverse('verReservas'))
        else:
            print(reservaForm.errors)
    else:
        reservaForm = ReservaForm()

    data = {
        'reservaForm': reservaForm,
        'titulo': 'Crear Reserva'
    }
    return render(request, 'blessedApp/crear_reservas.html', data)


def editarReserva(request, id):
    reserva = Reserva.objects.get(id=id)
    reservaForm = ReservaForm(instance=reserva, editar=True)

    if request.method == 'POST':
        reservaForm = ReservaForm(request.POST, instance=reserva, editar=True)
        if reservaForm.is_valid():
            print("Formulario válido")
            reserva_actualizada = reservaForm.save(commit=False)

            # 🔹 Verificar si el estado cambió a "Finalizado"
            estado_finalizado = Estado.objects.filter(estado__iexact="Finalizado").first()
            if estado_finalizado and reserva_actualizada.estado == estado_finalizado:
                # 🔓 Liberar disponibilidad del barbero en ese rango horario
                Disponibilidad.objects.filter(
                    barbero=reserva_actualizada.barbero,
                    fecha=reserva_actualizada.fecha,
                    hora_inicio__lte=reserva_actualizada.hora_fin,
                    hora_fin__gte=reserva_actualizada.hora_inicio
                ).update(disponible=True)
                print("✅ Disponibilidad liberada para el barbero.")

            reserva_actualizada.save()
            return HttpResponseRedirect(reverse('verReservas'))
        else:
            print("Formulario inválido", reservaForm.errors)

    data = {
        'reservaForm': reservaForm,
        'titulo': 'Editar Reserva'
    }
    return render(request, 'blessedApp/crear_reservas.html', data)


def eliminarReserva(request, id):
    reserva = Reserva.objects.get(id=id)
    reserva.delete()
    return HttpResponseRedirect(reverse('verReservas'))



def mostrarEstados(request):
    estados = Estado.objects.all()
    data = {
        'estados': estados,
        'titulo': 'Estados Disponibles'
    }
    return render (request, 'blessedApp/ver_estados.html',data)


def crearEstado(request):
    estadoForm = EstadoForm()

    if request.method == 'POST':
        estadoForm = EstadoForm(request.POST)
        if estadoForm.is_valid():
            print("Formulario válido")
            estadoForm.save()
            return HttpResponseRedirect(reverse('verEstados'))
    data = {
            'estadoForm': estadoForm,
            'titulo': 'Crear Estado'
        }
    return render(request, 'blessedApp/crear_estados.html', data)
    
def editarEstado(request, id):
    estado = Estado.objects.get(id=id)
    estadoForm = EstadoForm(instance=estado)
    if (request.method == 'POST'):
        estadoForm = EstadoForm(request.POST, instance=estado)
        if estadoForm.is_valid():
            print("Formulario válido")
            estadoForm.save()
            return HttpResponseRedirect(reverse('verEstados'))
        else:
            print("Formulario inválido", estadoForm.errors)
    data = {
        'estadoForm': estadoForm,
        'titulo': 'Editar Estado'
    }
    return render(request, 'blessedApp/crear_estados.html', data)

def eliminarEstado(request, id):
    estado = Estado.objects.get(id=id)
    estado.delete()
    return HttpResponseRedirect(reverse('verEstados'))


def cerrar_sesion(request):
    request.session.flush()
    messages.success(request, "Has cerrado sesión exitosamente.")
    return redirect('login')