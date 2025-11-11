from django.contrib.auth.hashers import make_password
from .models import Usuario, Rol

def crear_usuario_admin_por_defecto(sender, **kwargs):
    rol_admin, _ = Rol.objects.get_or_create(rol='Administrador')
    if not Usuario.objects.filter(usuario='admin').exists():
        Usuario.objects.create(
            usuario='admin',
            correo='admin@blessedapp.cl',
            telefono='11111111',
            rut='11111111-1',
            rol=rol_admin,
            password=make_password('admin')
        )