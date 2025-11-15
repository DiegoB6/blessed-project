from django.test import TestCase, Client
from .models import *
from django.contrib.auth.hashers import make_password
from django.urls import reverse



class TestModels(TestCase):

    def test_model_rol(self):
        rol_model = Rol.objects.create(
            rol = "Barbero"
        )
        self.assertEqual(str(rol_model), "Barbero")
        self.assertTrue(isinstance(rol_model, Rol))


    def test_model_rol_fallido(self):
        rol_model = Rol.objects.create(
            rol = 1234
        )
        self.assertEqual(str(rol_model), 1234)
        self.assertTrue(isinstance(rol_model, Rol))


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


    def test_acceso_panel_admin_sin_permisos(self):
        response = self.client.get(reverse("panel_admin"), follow=True)
        self.assertRedirects(response, "/login/")