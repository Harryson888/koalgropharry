# add_test_data.py
import os
import django
from datetime import date

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Koal_Group.settings')
django.setup()

from produccion_inventario.models import Empleado, Herramienta

# Crear empleados
empleado1 = Empleado.objects.create(
    nombres="Carlos",
    apellidos="Gómez",
    fecha_contratacion=date(2023, 1, 15),
    telefono="123456789",
    email="carlos@example.com",
    fecha_nacimiento=date(1990, 5, 20),
    rol="operador",
    estado="Activo"
)

empleado2 = Empleado.objects.create(
    nombres="Ana",
    apellidos="Martínez",
    fecha_contratacion=date(2022, 6, 10),
    telefono="987654321",
    email="ana@example.com",
    fecha_nacimiento=date(1985, 3, 12),
    rol="minero",
    estado="Activo"
)

# Crear herramientas
Herramienta.objects.create(
    nombre="Martillo",
    descripcion="Martillo de acero",
    estado="asignada",
    empleado=empleado1,
    fecha_asignacion=date(2025, 4, 1),
    fecha_devolucion=None
)

Herramienta.objects.create(
    nombre="Taladro",
    descripcion="Taladro eléctrico",
    estado="en_mantenimiento",
    empleado=None,
    fecha_asignacion=None,
    fecha_devolucion=None
)

Herramienta.objects.create(
    nombre="Pala",
    descripcion="Pala de punta fina",
    estado="asignada",
    empleado=empleado2,
    fecha_asignacion=date(2025, 3, 15),
    fecha_devolucion=None
)

print("Datos de prueba creados exitosamente.")