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
