from django.apps import AppConfig


class BlessedappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blessedApp'
    
    def ready(self):
        from django.db.models.signals import post_migrate
        from .signals import crear_usuario_admin_por_defecto
        post_migrate.connect(crear_usuario_admin_por_defecto, sender=self)


