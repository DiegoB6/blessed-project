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

from django.db.models import Count
import json
from django.core.serializers.json import DjangoJSONEncoder

# pip install reportlab
# from reportlab.pdfgen import canvas
# from django.http import HttpResponse, FileResponse

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


@rol_requerido(['Administrador'])
def mostrarRoles(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        messages.error(request, "Debe iniciar sesión para acceder.")
        return redirect('login')

    roles = Rol.objects.all()
    data = {
        'roles': roles,
        'titulo': 'Roles Disponibles'
    }
    return render (request, 'blessedApp/ver_roles.html',data)


@rol_requerido(['Administrador'])
def crearRol(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        messages.error(request, "Debe iniciar sesión para acceder.")
        return redirect('login')
    
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
    
@rol_requerido(['Administrador'])
def editarRol(request, id):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        messages.error(request, "Debe iniciar sesión para acceder.")
        return redirect('login')

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

@rol_requerido(['Administrador'])
def eliminarRol(request, id):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        messages.error(request, "Debe iniciar sesión para acceder.")
        return redirect('login')

    rol = Rol.objects.get(id=id)
    rol.delete()
    return HttpResponseRedirect(reverse('verRoles'))
            


@rol_requerido(['Administrador'])
def mostrarServicios(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        messages.error(request, "Debe iniciar sesión para acceder.")
        return redirect('login')

    servicios = Servicio.objects.all()
    data = {
        'servicios': servicios,
        'titulo': 'Servicios Disponibles'
    }
    return render (request, 'blessedApp/ver_servicios.html',data)


@rol_requerido(['Administrador'])
def crearServicio(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        messages.error(request, "Debe iniciar sesión para acceder.")
        return redirect('login')

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

@rol_requerido(['Administrador'])
def editarServicio(request, id):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        messages.error(request, "Debe iniciar sesión para acceder.")
        return redirect('login')

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

@rol_requerido(['Administrador'])
def eliminarServicio(request, id):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        messages.error(request, "Debe iniciar sesión para acceder.")
        return redirect('login')

    servicio = Servicio.objects.get(id=id)
    servicio.delete()
    return HttpResponseRedirect(reverse('verServicios'))


@rol_requerido(['Administrador'])
def mostrarUsuarios(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        messages.error(request, "Debe iniciar sesión para acceder.")
        return redirect('login')

    usuarios = Usuario.objects.all()
    data = {
        'usuarios': usuarios,
        'titulo': 'Usuarios Disponibles'
    }
    return render (request, 'blessedApp/ver_usuarios.html',data)


@rol_requerido(['Administrador'])
def crearUsuario(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        messages.error(request, "Debe iniciar sesión para acceder.")
        return redirect('login')

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
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        messages.error(request, "Debe iniciar sesión para acceder.")
        return redirect('login')

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


@rol_requerido(['Administrador'])
def eliminarUsuario(request, id):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        messages.error(request, "Debe iniciar sesión para acceder.")
        return redirect('login')

    usuario = Usuario.objects.get(id=id)
    usuario.delete()
    return HttpResponseRedirect(reverse('verUsuarios'))



@rol_requerido(['Administrador', 'Barbero'])
def mostrarDisponibilidades(request):
    usuario_id = request.session.get('usuario_id')

    if not usuario_id:
        messages.error(request, "Debe iniciar sesión para ver sus disponibilidades.")
        return redirect('login')

    usuario = Usuario.objects.get(id=usuario_id)

    #  Si el usuario es barbero → mostrar solo sus disponibilidades
    if usuario.rol.rol.lower() == 'barbero':
        disponibilidades = Disponibilidad.objects.filter(barbero=usuario)
    else:
        #  Si es admin → mostrar todas
        disponibilidades = Disponibilidad.objects.all()

    context = {
        'disponibilidades': disponibilidades,
        'titulo': 'Mis Disponibilidades' if usuario.rol.rol.lower() == 'barbero' else 'Disponibilidades'
    }

    return render(request, 'blessedApp/ver_disponibilidades.html', context)

@rol_requerido(['Administrador', 'Barbero'])
def crearDisponibilidad(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        messages.error(request, "Debe iniciar sesión para crear una disponibilidad.")
        return redirect('login')

    usuario = Usuario.objects.get(id=usuario_id)

    if request.method == 'POST':
        disponibilidadForm = DisponibilidadForm(request.POST, usuario=usuario)
        if disponibilidadForm.is_valid():
            disponibilidad = disponibilidadForm.save(commit=False)

            #  Si el usuario logueado es barbero, asignarlo automáticamente
            if usuario.rol.rol.lower() == 'barbero':
                disponibilidad.barbero = usuario

            disponibilidad.save()
            messages.success(request, "✅ Disponibilidad creada correctamente.")
            return HttpResponseRedirect(reverse('verDisponibilidades'))
        else:
            print("Formulario inválido", disponibilidadForm.errors)
    else:
        disponibilidadForm = DisponibilidadForm(usuario=usuario)

    data = {
        'disponibilidadForm': disponibilidadForm,
        'titulo': 'Crear Disponibilidad'
    }
    return render(request, 'blessedApp/crear_disponibilidades.html', data)


def editarDisponibilidad(request, id):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        messages.error(request, "Debe iniciar sesión para editar una disponibilidad.")
        return redirect('login')

    usuario = Usuario.objects.get(id=usuario_id)
    disponibilidad = Disponibilidad.objects.get(id=id)

    # Pasamos el usuario al formulario
    if request.method == 'POST':
        disponibilidadForm = DisponibilidadForm(request.POST, instance=disponibilidad, usuario=usuario)
        if disponibilidadForm.is_valid():
            print("Formulario válido")
            disponibilidad_editada = disponibilidadForm.save(commit=False)

            # Si el usuario es barbero, forzamos que la disponibilidad quede asociada a él
            if usuario.rol.rol.lower() == 'barbero':
                disponibilidad_editada.barbero = usuario

            disponibilidad_editada.save()
            messages.success(request, "✅ Disponibilidad actualizada correctamente.")
            return HttpResponseRedirect(reverse('verDisponibilidades'))
        else:
            print("Formulario inválido", disponibilidadForm.errors)
    else:
        disponibilidadForm = DisponibilidadForm(instance=disponibilidad, usuario=usuario)

    data = {
        'disponibilidadForm': disponibilidadForm,
        'titulo': 'Editar Disponibilidad'
    }
    return render(request, 'blessedApp/crear_disponibilidades.html', data)


def eliminarDisponibilidad(request, id):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        messages.error(request, "Debe iniciar sesión para acceder.")
        return redirect('login')

    disponibilidad = Disponibilidad.objects.get(id=id)
    disponibilidad.delete()
    return HttpResponseRedirect(reverse('verDisponibilidades'))


@rol_requerido(['Administrador'])
def mostrarReservas(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        messages.error(request, "Debe iniciar sesión para acceder.")
        return redirect('login')

    reservas = Reserva.objects.all()
    data = {
        'reservas': reservas,
        'titulo': 'Reservas Disponibles'
    }
    return render (request, 'blessedApp/ver_reservas.html',data)


@rol_requerido(['Administrador', 'Cliente']) 
def crearReserva(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        messages.error(request, "Debe iniciar sesión para crear una reserva.")
        return redirect('login')

    cliente = Usuario.objects.get(id=usuario_id)

    #  Determinar si el usuario es Administrador
    es_admin = cliente.rol.rol.lower() == "administrador"

    if request.method == 'POST':
        # Si es admin, puede ver todos los campos; si no, se ocultan cliente y estado
        reservaForm = ReservaForm(request.POST, admin=es_admin)
        if reservaForm.is_valid():
            reserva = reservaForm.save(commit=False)

            # Si no es admin, asigna el cliente logueado automáticamente
            if not es_admin:
                reserva.cliente = cliente

                # Asigna estado "Pendiente" automáticamente
                estado_pendiente, _ = Estado.objects.get_or_create(estado="Pendiente")
                reserva.estado = estado_pendiente

            #  Verificar disponibilidad del barbero
            disponibilidad_ocupada = Disponibilidad.objects.filter(
                barbero=reserva.barbero,
                fecha=reserva.fecha,
                hora_inicio__lte=reserva.hora_inicio,
                hora_fin__gte=reserva.hora_inicio,
                disponible=False
            ).exists()

            if disponibilidad_ocupada:
                messages.error(request, "El barbero no está disponible en el horario seleccionado.")
                data = {
                    'reservaForm': reservaForm,
                    'titulo': 'Crear Reserva'
                }
                return render(request, 'blessedApp/crear_reservas.html', data)

            reserva.save()
            messages.success(request, "Reserva creada exitosamente.")
            if es_admin:
                return redirect('verReservas')
            else:
                return redirect('verReservasCliente')
        else:
            print(reservaForm.errors)
    else:
        reservaForm = ReservaForm(admin=es_admin)

    data = {
        'reservaForm': reservaForm,
        'titulo': 'Crear Reserva'
    }
    return render(request, 'blessedApp/crear_reservas.html', data)


@rol_requerido(['Administrador'])
def editarReserva(request, id):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        messages.error(request, "Debe iniciar sesión para acceder.")
        return redirect('login')

    reserva = Reserva.objects.get(id=id)
    reservaForm = ReservaForm(instance=reserva, editar=True)

    if request.method == 'POST':
        reservaForm = ReservaForm(request.POST, instance=reserva, editar=True)
        if reservaForm.is_valid():
            print("Formulario válido")
            reserva_actualizada = reservaForm.save(commit=False)

            #  Verificar si el estado cambió a "Finalizado"
            estado_finalizado = Estado.objects.filter(estado__iexact="Finalizado").first()
            if estado_finalizado and reserva_actualizada.estado == estado_finalizado:
                #  Liberar disponibilidad del barbero en ese rango horario
                Disponibilidad.objects.filter(
                    barbero=reserva_actualizada.barbero,
                    fecha=reserva_actualizada.fecha,
                    hora_inicio__lte=reserva_actualizada.hora_fin,
                    hora_fin__gte=reserva_actualizada.hora_inicio
                ).update(disponible=True)
                print("Disponibilidad liberada para el barbero.")

            reserva_actualizada.save()
            return HttpResponseRedirect(reverse('verReservas'))
        else:
            print("Formulario inválido", reservaForm.errors)

    data = {
        'reservaForm': reservaForm,
        'titulo': 'Editar Reserva'
    }
    return render(request, 'blessedApp/crear_reservas.html', data)


@rol_requerido(['Administrador'])
def eliminarReserva(request, id):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        messages.error(request, "Debe iniciar sesión para acceder.")
        return redirect('login')

    reserva = Reserva.objects.get(id=id)
    reserva.liberar_disponibilidad()
    reserva.delete()
    return HttpResponseRedirect(reverse('verReservas'))


@rol_requerido(['Cliente'])
def eliminarReservaCliente(request, id):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        messages.error(request, "Debe iniciar sesión para acceder.")
        return redirect('login')

    reserva = Reserva.objects.get(id=id)
    reserva.liberar_disponibilidad()
    reserva.delete()
    return HttpResponseRedirect(reverse('verReservasCliente'))


@rol_requerido(['Barbero'])
def eliminarReservaBarbero(request, id):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        messages.error(request, "Debe iniciar sesión para acceder.")
        return redirect('login')

    reserva = Reserva.objects.get(id=id)
    reserva.liberar_disponibilidad()
    reserva.delete()
    return HttpResponseRedirect(reverse('verReservasBarbero'))



@rol_requerido(['Administrador'])
def mostrarEstados(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        messages.error(request, "Debe iniciar sesión para acceder.")
        return redirect('login')

    estados = Estado.objects.all()
    data = {
        'estados': estados,
        'titulo': 'Estados Disponibles'
    }
    return render (request, 'blessedApp/ver_estados.html',data)


@rol_requerido(['Administrador'])
def crearEstado(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        messages.error(request, "Debe iniciar sesión para acceder.")
        return redirect('login')

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

@rol_requerido(['Administrador'])    
def editarEstado(request, id):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        messages.error(request, "Debe iniciar sesión para acceder.")
        return redirect('login')

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

@rol_requerido(['Administrador'])
def eliminarEstado(request, id):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        messages.error(request, "Debe iniciar sesión para acceder.")
        return redirect('login')

    estado = Estado.objects.get(id=id)
    estado.delete()
    return HttpResponseRedirect(reverse('verEstados'))


def cerrar_sesion(request):
    request.session.flush()
    messages.success(request, "Has cerrado sesión exitosamente.")
    return redirect('login')


@rol_requerido(['Barbero'])
def editarReservaBarbero(request, id):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        messages.error(request, "Debe iniciar sesión para acceder.")
        return redirect('login')

    reserva = Reserva.objects.get(id=id)
    reservaForm = ReservaForm(instance=reserva, editar=True, solo_estado=True)

    if request.method == 'POST':
        reservaForm = ReservaForm(request.POST, instance=reserva, editar=True, solo_estado=True)
        if reservaForm.is_valid():
            reservaForm.save()
            messages.success(request, "Estado de la reserva actualizado correctamente.")
            return HttpResponseRedirect(reverse('verReservasBarbero'))
        else:
            print("Formulario inválido", reservaForm.errors)

    data = {
        'reservaForm': reservaForm,
        'titulo': 'Actualizar Reserva'
    }
    return render(request, 'blessedApp/crear_reservas.html', data)


@rol_requerido(['Cliente'])
def mostrarReservasCliente(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        messages.error(request, "Debe iniciar sesión para acceder.")
        return redirect('login')

    usuario_id = request.session.get('usuario_id')
    reservas = Reserva.objects.filter(cliente_id=usuario_id)

    data = {
        'reservas': reservas,
        'titulo': 'Mis Reservas'
    }
    return render(request, 'blessedApp/ver_reservas_clientes.html', data)


@rol_requerido(['Barbero'])
def mostrarReservasBarbero(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        messages.error(request, "Debe iniciar sesión para acceder.")
        return redirect('login')

    usuario_id = request.session.get('usuario_id')
    reservas = Reserva.objects.filter(barbero_id=usuario_id)

    data = {
        'reservas': reservas,
        'titulo': 'Mis Reservas'
    }
    return render(request, 'blessedApp/ver_reservas_barberos.html', data)


def crearCliente(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)

        #  Eliminar el campo 'rol' ANTES de validar
        if 'rol' in form.fields:
            form.fields.pop('rol')

        if form.is_valid():
            usuario = form.save(commit=False)

            # Asignar automáticamente el rol "Cliente"
            rol_cliente, _ = Rol.objects.get_or_create(rol__iexact="Cliente", defaults={'rol': 'Cliente'})
            usuario.rol = rol_cliente

            usuario.save()
            messages.success(request, "Usuario registrado correctamente.")
            return redirect(reverse('login'))  # o la ruta que prefieras
        else:
            print("Errores del formulario:", form.errors)
            messages.error(request, "Corrige los errores del formulario.")
    else:
        form = UsuarioForm()
        if 'rol' in form.fields:
            form.fields.pop('rol')

    data = {
        'usuarioForm': form,
        'titulo': 'Registro de Cliente'
    }
    return render(request, 'registration/crear_cliente.html', data)


def editarDatos(request):
    usuario_id = request.session.get('usuario_id')

    if not usuario_id:
        messages.error(request, "Debe iniciar sesión para editar su perfil.")
        return redirect('login')

    usuario = Usuario.objects.get(id=usuario_id)

    if usuario.rol == "Cliente":
        default_next = reverse("panel_cliente")
    elif usuario.rol == "Barbero":
        default_next = reverse("panel_barbero")
    elif usuario.rol == "Admin":
        default_next = reverse("panel_admin")
    else:
        default_next = reverse("login")

    next_url = request.GET.get('next') or request.POST.get('next') or default_next

    if request.method == 'POST':
        form = EditarDatosUsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil actualizado correctamente.")
            return redirect(next_url or reverse('login')) 
        else:
            print("Formulario inválido:", form.errors)
            messages.error(request, "Corrige los errores del formulario.")
    else:
        form = EditarDatosUsuarioForm(instance=usuario)

    data = {
        'editarDatosForm': form,
        'titulo': 'Editar Perfil',
        'next': next_url,
    }
    return render(request, 'registration/editar_perfil.html', data)


def cambiarPassword(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        messages.error(request, "Debe iniciar sesión para acceder.")
        return redirect('login')

    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        messages.error(request, "Debe iniciar sesión para cambiar su contraseña.")
        return redirect('login')

    usuario = Usuario.objects.get(id=usuario_id)

    if request.method == 'POST':
        cambiarPasswordForm = CambiarPasswordForm(usuario, request.POST)
        if cambiarPasswordForm.is_valid():
            nueva_contrasena = cambiarPasswordForm.cleaned_data['nueva_contrasena']
            usuario.password = make_password(nueva_contrasena)
            usuario.save()
            messages.success(request, "Tu contraseña ha sido actualizada correctamente.")
            return redirect('login') 
    else:
        cambiarPasswordForm = CambiarPasswordForm(usuario)

    data = {
        'cambiarPasswordForm': cambiarPasswordForm,
        'titulo': 'Cambiar Contraseña'
    }
    return render(request, 'registration/cambiar_password.html', data)


@rol_requerido(['Administrador'])
def crearReservaAdmin(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        messages.error(request, "Debe iniciar sesión para acceder.")
        return redirect('login')

    reservaForm = ReservaForm()

    if request.method == 'POST':
        reservaForm = ReservaForm(request.POST)
        if reservaForm.is_valid():
            print("Formulario válido")
            reservaForm.save()
            return HttpResponseRedirect(reverse('verReservas'))
    data = {
            'reservaForm': reservaForm,
            'titulo': 'Crear Reserva'
        }
    return render(request, 'blessedApp/crear_reservas.html', data)


@rol_requerido(['Barbero'])
def mostrarDisponibilidadesBarbero(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        messages.error(request, "Debe iniciar sesión para acceder.")
        return redirect('login')

    disponibilidades = Disponibilidad.objects.all()
    data = {
        'disponibilidades': disponibilidades,
        'titulo': 'Disponibilidades Disponibles'
    }
    return render (request, 'blessedApp/ver_disponibilidades.html',data)



@rol_requerido(['Administrador'])
def graficos(request):

    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        messages.error(request, "Debe iniciar sesión para acceder a los gráficos.")
        return redirect('login')

    # KPI 1 – HORARIOS MÁS SOLICITADOS
    horarios_solicitados = (
        Reserva.objects.values("hora_inicio")
        .annotate(total=Count("id"))
        .order_by("-total")[:10]
    )

    # KPI 2 – SERVICIOS MÁS SOLICITADOS
    servicios_populares = (
        Reserva.objects.values("servicio__servicio")
        .annotate(total=Count("id"))
        .order_by("-total")
    )

    # KPI 3 – BARBERO CON MÁS CLIENTES
    barberos_con_clientes = (
        Reserva.objects.values("barbero__usuario")
        .annotate(total_clientes=Count("cliente"))
        .order_by("-total_clientes")
)

    top_barbero = barberos_con_clientes[0] if barberos_con_clientes else None

    # Convertimos datos a JSON

    horarios_labels = [str(h["hora_inicio"]) for h in horarios_solicitados]
    horarios_data = [h["total"] for h in horarios_solicitados]

    servicios_labels = [s["servicio__servicio"] for s in servicios_populares]
    servicios_data = [s["total"] for s in servicios_populares]

    data = {
        # Datos crudos por si los necesitas en HTML
        "top_barbero": top_barbero,

        # Datos convertidos a JSON (para Chart.js)
        "horarios_labels": json.dumps(horarios_labels, cls=DjangoJSONEncoder),
        "horarios_data": json.dumps(horarios_data, cls=DjangoJSONEncoder),
        "servicios_labels": json.dumps(servicios_labels, cls=DjangoJSONEncoder),
        "servicios_data": json.dumps(servicios_data, cls=DjangoJSONEncoder),
    }

    return render(request, "blessedApp/graficos.html", data)


def volverPanel(request):
    usuario_id = request.session.get('usuario_id')

    if not usuario_id:
        return redirect('login')

    usuario = Usuario.objects.get(id=usuario_id)
    rol = usuario.rol.rol.lower()

    if rol == "administrador":
        return redirect('panel_admin')
    elif rol == "barbero":
        return redirect('panel_barbero')
    else:
        return redirect('panel_cliente')