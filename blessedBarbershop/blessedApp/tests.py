from django.test import TestCase, Client
from .models import *
from django.contrib.auth.hashers import make_password
from django.urls import reverse



class TestModels(TestCase):

    # Prueba correcta para el modelo (tabla) Rol, en este caso se crea un rol de barbero 
    # y se verifica que se haya creado correctamente.
    def test_model_rol(self):
        rol_model = Rol.objects.create(
            rol = "Barbero"
        )
        self.assertEqual(str(rol_model), "Barbero")
        self.assertTrue(isinstance(rol_model, Rol))


    # Prueba fallida para el modelo (tabla) Rol, en este caso se intenta crear un rol con un valor numérico 
    # en lugar de string que es el tipo de dato definido y se verifica que no se haya creado mostrando un error
    def test_model_rol_fallido(self):
        rol_model = Rol.objects.create(
            rol = 1234
        )
        self.assertEqual(str(rol_model), 1234)
        self.assertTrue(isinstance(rol_model, Rol))


# Se definen datos de prueba para testear el login de usuarios, en este caso creando un usuario test con rol de cliente y campos necesarios.
class TestLogin(TestCase):
    def setUp(self):
        self.rol = Rol.objects.create(rol="Cliente")
        self.usuario = Usuario.objects.create(
            usuario="testuser",
            correo="testuser@gmail.com",
            telefono=123456789,
            password=make_password("1234"),
            rol=self.rol
        )

    # Prueba correcta para el login de usuario, en este caso se intenta iniciar sesión con las credenciales correctas
    #  y se verifica que la sesión se haya iniciado correctamente.
    def test_login_exitoso(self):
        response = self.client.post(
            reverse("login"),
            {"usuario": "testuser", "password": "1234"},
            follow=True
        )
        session = self.client.session

        self.assertEqual(response.status_code, 200)

        self.assertIn("usuario_id", session)
        self.assertIn("usuario_nombre", session)
        self.assertIn("rol", session)


    # Prueba fallida para el login de usuario, en este caso se intenta iniciar sesión con credenciales incorrectas y se valida que no 
    # inicio sesion correctamente mostrando el error.
    def test_login_fallido(self):
        response = self.client.post(
            reverse("login"),
            {"usuario": "fallo", "password": "fallo"},
            follow=True
        )
        session = self.client.session

        self.assertEqual(response.status_code, 200)

        self.assertIn("usuario_id", session)
        self.assertIn("usuario_nombre", session)
        self.assertIn("rol", session)


    # Prueba de acceso al panel de administración sin permisos, en este caso se intenta acceder al panel sin haber iniciado sesión y muestra un error
    def test_acceso_panel_admin_sin_permisos(self):
        response = self.client.get(reverse("panel_admin"), follow=True)
        self.assertRedirects(response, "/login/")