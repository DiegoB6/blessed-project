from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password, check_password

class Servicio(models.Model):
    servicio = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=100)
    precio = models.IntegerField()

    def __str__(self):
        return self.servicio


class Rol(models.Model):
    rol = models.CharField(max_length=50)

    def __str__(self):
        return self.rol


class Usuario(models.Model):
    usuario = models.CharField(max_length=50, unique=True)
    correo = models.EmailField()
    telefono = models.IntegerField()
    password = models.CharField(max_length=100)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # Solo hashea la contraseña si no está ya hasheada
        if not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.usuario


class Disponibilidad(models.Model):
    barbero = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='disponibilidades')
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.barbero.usuario} - {self.fecha} ({self.hora_inicio} - {self.hora_fin})"


class Reserva(models.Model):
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    estado = models.CharField(max_length=20)
    cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='cliente')
    barbero = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='barbero')
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)

    def clean(self):
        # Validar que exista disponibilidad activa para ese barbero en ese horario
        disponibilidad = Disponibilidad.objects.filter(
            barbero=self.barbero,
            fecha=self.fecha,
            hora_inicio__lte=self.hora_inicio,
            hora_fin__gte=self.hora_fin,
            disponible=True
        ).first()

        if not disponibilidad:
            raise ValidationError("El barbero no está disponible en el horario seleccionado.")

    def save(self, *args, **kwargs):
        self.clean()  # Valida antes de guardar

        super().save(*args, **kwargs)

        # Actualizar disponibilidad: marcar como ocupada
        Disponibilidad.objects.filter(
            barbero=self.barbero,
            fecha=self.fecha,
            hora_inicio__lte=self.hora_inicio,
            hora_fin__gte=self.hora_fin,
            disponible=True
        ).update(disponible=False)

    def __str__(self):
        return f"Reserva {self.id} - {self.cliente.usuario} con {self.barbero.usuario}"
