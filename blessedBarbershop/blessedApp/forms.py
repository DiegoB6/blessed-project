from django import forms 
from blessedApp.models import *

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
        super().__init__(*args, **kwargs)
        # Filtra los usuarios que tienen el rol 'Barbero'
        self.fields['barbero'].queryset = Usuario.objects.filter(rol__rol__iexact='Barbero')
        self.fields['barbero'].widget.attrs.update({'class': 'form-select'})