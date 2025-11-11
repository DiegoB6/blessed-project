from datetime import datetime, timedelta
from django import forms 
from blessedApp.models import *

class EstadoForm(forms.ModelForm):
    estado = forms.CharField(label='Estado', max_length=25)
    estado.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Estado
        fields= '__all__'


class RolForm(forms.ModelForm):
    rol = forms.CharField(label='Rol', max_length=25)
    rol.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Rol
        fields= '__all__'

class ServicioForm(forms.ModelForm):
    servicio = forms.CharField(label='Servicio', max_length=50)
    descripcion = forms.CharField(label='Descripción', max_length=100)
    precio = forms.IntegerField(label='Precio')

    servicio.widget.attrs['class'] = 'form-control'
    descripcion.widget.attrs['class'] = 'form-control'
    precio.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Servicio
        fields= '__all__'


class UsuarioForm(forms.ModelForm):
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Usuario
        fields = ['usuario', 'correo', 'telefono', 'password', 'rol']
        widgets = {
            'usuario': forms.TextInput(attrs={'class': 'form-control'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.NumberInput(attrs={'class': 'form-control'}),
            'rol': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_password(self):
        """Hashea la contraseña antes de guardar,
        evitando duplicar el hash si ya está cifrada."""
        password = self.cleaned_data.get('password')
        if not password.startswith('pbkdf2_sha256$'):
            return make_password(password)
        return password
    

class EditarDatosUsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['usuario', 'correo', 'telefono']


class DisponibilidadForm(forms.ModelForm):
    class Meta:
        model = Disponibilidad
        fields = ['barbero', 'fecha', 'hora_inicio', 'hora_fin', 'disponible']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hora_inicio': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'hora_fin': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'disponible': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        usuario = kwargs.pop('usuario', None)
        super().__init__(*args, **kwargs)
        # Filtra los usuarios que tienen el rol 'Barbero'
        self.fields['barbero'].queryset = Usuario.objects.filter(rol__rol__iexact='Barbero')
        self.fields['barbero'].widget.attrs.update({'class': 'form-select'})

         # Si el usuario está definido y es barbero, ocultamos el campo 'barbero'
        if usuario and usuario.rol.rol.lower() == 'barbero':
            self.fields.pop('barbero')
        else:
            # Mostrar solo los barberos en el select si el usuario es admin
            self.fields['barbero'].queryset = Usuario.objects.filter(rol__rol__iexact='barbero')






class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['fecha', 'hora_inicio', 'barbero', 'servicio', 'estado', 'cliente']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hora_inicio': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'barbero': forms.Select(attrs={'class': 'form-control'}),
            'servicio': forms.Select(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'cliente': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        editar = kwargs.pop('editar', False)
        solo_estado = kwargs.pop('solo_estado', False)
        admin = kwargs.pop('admin', False)
        super().__init__(*args, **kwargs)

        # Mostrar solo barberos
        self.fields['barbero'].queryset = Usuario.objects.filter(rol__rol__iexact='barbero')

        # Mostrar solo clientes en el campo cliente
        self.fields['cliente'].queryset = Usuario.objects.filter(rol__rol__iexact='cliente')

        # 🔹 Si el formulario es solo para editar el estado
        if solo_estado:
            for field in list(self.fields.keys()):
                if field != 'estado':
                    self.fields.pop(field)

        # 🔹 Si no es modo editar ni admin → ocultar cliente y estado
        elif not editar and not admin:
            self.fields.pop('cliente')
            self.fields.pop('estado')

    def save(self, commit=True):
        reserva = super().save(commit=False)

        # Calcular hora_fin automáticamente
        if not reserva.hora_fin:
            reserva.hora_fin = (datetime.combine(reserva.fecha, reserva.hora_inicio) + timedelta(hours=1)).time()

        # Asignar estado "Pendiente" por defecto si no tiene uno
        if not reserva.estado_id:
            estado_pendiente, _ = Estado.objects.get_or_create(estado="Pendiente")
            reserva.estado = estado_pendiente

        if commit:
            reserva.save()
        return reserva



class CambiarPasswordForm(forms.Form):
    contrasena_actual = forms.CharField(
        label="Contraseña actual",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    nueva_contrasena = forms.CharField(
        label="Nueva contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    confirmar_contrasena = forms.CharField(
        label="Confirmar nueva contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    def __init__(self, usuario, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.usuario = usuario

    def clean(self):
        cleaned_data = super().clean()
        contrasena_actual = cleaned_data.get('contrasena_actual')
        nueva_contrasena = cleaned_data.get('nueva_contrasena')
        confirmar_contrasena = cleaned_data.get('confirmar_contrasena')

        #  Verificar contraseña actual
        if not check_password(contrasena_actual, self.usuario.password):
            raise forms.ValidationError("La contraseña actual es incorrecta.")

        #  Verificar coincidencia
        if nueva_contrasena != confirmar_contrasena:
            raise forms.ValidationError("Las contraseñas nuevas no coinciden.")

        return cleaned_data
    


    

class ReservaAdminForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['fecha', 'hora_inicio', 'barbero', 'servicio', 'estado', 'cliente']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hora_inicio': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'barbero': forms.Select(attrs={'class': 'form-control'}),
            'servicio': forms.Select(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'cliente': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Mostrar solo barberos y clientes correctos
        self.fields['barbero'].queryset = Usuario.objects.filter(rol__rol__iexact='barbero')
        self.fields['cliente'].queryset = Usuario.objects.filter(rol__rol__iexact='cliente')

    def save(self, commit=True):
        reserva = super().save(commit=False)

        # Calcular hora_fin automáticamente
        if not reserva.hora_fin:
            reserva.hora_fin = (datetime.combine(reserva.fecha, reserva.hora_inicio) + timedelta(hours=1)).time()

        # Asignar estado "Pendiente" por defecto si no tiene uno
        if not reserva.estado_id:
            estado_pendiente, _ = Estado.objects.get_or_create(estado="Pendiente")
            reserva.estado = estado_pendiente

        if commit:
            reserva.save()
        return reserva