from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.conf import settings
from .models import Usuario, Rol
import sys


@receiver(post_migrate)
def crear_usuario_admin_por_defecto(sender, **kwargs):
    """
    Crea un usuario administrador solo si:
    - No existe ya uno en la base de datos.
    - No se están ejecutando pruebas automáticas.
    """
    # 🚫 Evita crear el admin durante los tests
    if 'test' in sys.argv:
        return

    # Crear rol de administrador si no existe
    rol_admin, _ = Rol.objects.get_or_create(rol="Administrador")

    # Crear usuario admin si no existe
    if not Usuario.objects.filter(usuario="admin").exists():
        Usuario.objects.create(
            usuario="admin",
            correo="admin@blessed.cl",
            telefono=123456789,
            password="admin123",
            rol=rol_admin
        )
