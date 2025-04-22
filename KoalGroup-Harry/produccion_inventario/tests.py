# produccion_inventario/tests.py
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Proyecto, ControlIngreso, Empleado, Verificacion, ListaChequeo, Herramienta, UserProfile
from datetime import date

class HerramientasAsignadasTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Crear un usuario supervisor
        self.supervisor = User.objects.create_user(username='supervisor', password='testpass123')
        self.supervisor_profile = UserProfile.objects.create(user=self.supervisor, rol='supervisor')
        # Crear un usuario no supervisor
        self.operador = User.objects.create_user(username='operador', password='testpass123')
        self.operador_profile = UserProfile.objects.create(user=self.operador, rol='operador')
        # Crear un empleado
        self.empleado = Empleado.objects.create(
            nombres="Carlos",
            apellidos="Gómez",
            fecha_contratacion=date(2023, 1, 15),
            telefono="123456789",
            email="carlos@example.com",
            fecha_nacimiento=date(1990, 5, 20),
            rol="operador",
            estado="Activo"
        )
        # Crear una herramienta
        self.herramienta = Herramienta.objects.create(
            nombre="Martillo",
            descripcion="Martillo de acero",
            estado="disponible"
        )

    def test_acceso_supervisor(self):
        self.client.login(username='supervisor', password='testpass123')
        response = self.client.get(reverse('herramientas_asignadas'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'produccion_inventario/herramientas_asignadas.html')

    def test_acceso_no_supervisor(self):
        self.client.login(username='operador', password='testpass123')
        response = self.client.get(reverse('herramientas_asignadas'))
        self.assertEqual(response.status_code, 403)  # Forbidden

    def test_asignar_herramienta(self):
        self.client.login(username='supervisor', password='testpass123')
        response = self.client.post(reverse('herramientas_asignadas'), {
            'action': 'asignar',
            'herramienta_id': self.herramienta.id,
            'empleado': self.empleado.id,
            'fecha_asignacion': '2025-04-08',
            'fecha_devolucion': '2025-04-15',
        })
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.herramienta.refresh_from_db()
        self.assertEqual(self.herramienta.empleado, self.empleado)
        self.assertEqual(self.herramienta.estado, 'asignada')
        self.assertEqual(str(self.herramienta.fecha_asignacion), '2025-04-08')
        self.assertEqual(str(self.herramienta.fecha_devolucion), '2025-04-15')

    def test_desasignar_herramienta(self):
        # Primero asignar la herramienta
        self.herramienta.empleado = self.empleado
        self.herramienta.estado = 'asignada'
        self.herramienta.fecha_asignacion = date(2025, 4, 8)
        self.herramienta.fecha_devolucion = date(2025, 4, 15)
        self.herramienta.save()

        self.client.login(username='supervisor', password='testpass123')
        response = self.client.post(reverse('herramientas_asignadas'), {
            'action': 'asignar',
            'herramienta_id': self.herramienta.id,
            'empleado': '',  # Unassign
            'fecha_asignacion': '',
            'fecha_devolucion': '',
        })
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.herramienta.refresh_from_db()
        self.assertIsNone(self.herramienta.empleado)
        self.assertEqual(self.herramienta.estado, 'disponible')
        self.assertIsNone(self.herramienta.fecha_asignacion)
        self.assertIsNone(self.herramienta.fecha_devolucion)

    def test_actualizar_estado_herramienta(self):
        self.client.login(username='supervisor', password='testpass123')
        response = self.client.post(reverse('herramientas_asignadas'), {
            'action': 'actualizar_estado',
            'herramienta_id': self.herramienta.id,
            'estado': 'en_mantenimiento',
        })
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.herramienta.refresh_from_db()
        self.assertEqual(self.herramienta.estado, 'en_mantenimiento')