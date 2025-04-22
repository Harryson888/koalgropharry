# produccion_inventario/models.py
from django.db import models
from django.contrib.auth.models import User

# Modelos existentes
class Proyecto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

# produccion_inventario/models.py
class Empleado(models.Model):
    nombre = models.CharField(max_length=100)
    identificacion = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=15)
    rol = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre
class Cargo(models.Model):
    nombre_cargo = models.CharField(max_length=100)
    descripcion = models.TextField()
    nivel = models.IntegerField()
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name='cargos')

    def __str__(self):
        return self.nombre_cargo

class ControlIngreso(models.Model):
    fecha = models.DateField()
    hora_entrada = models.TimeField()
    hora_salida = models.TimeField(null=True, blank=True)
    cantidad = models.IntegerField()
    categoria = models.CharField(max_length=100)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='ingresos')
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name='ingresos')

    def __str__(self):
        return f"Ingreso {self.id} - {self.proyecto.nombre}"

class Verificacion(models.Model):
    fecha_verificacion = models.DateField()
    estado = models.CharField(max_length=50)
    observaciones = models.TextField()
    control_ingreso = models.ForeignKey(ControlIngreso, on_delete=models.CASCADE, related_name='verificaciones')

    def __str__(self):
        return f"Verificación {self.id} - {self.control_ingreso.id}"

class ListaChequeo(models.Model):
    fecha_chequeo = models.DateField()
    categoria = models.CharField(max_length=100)
    resultado = models.CharField(max_length=100)
    observaciones = models.TextField()
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name='chequeos')

    def __str__(self):
        return f"Chequeo {self.id} - {self.empleado}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.CharField(max_length=20, choices=[
        ('supervisor', 'Supervisor'),
        ('trabajador', 'Trabajador'),
    ])

    def __str__(self):
        return f"{self.user.username} - {self.rol}"


    def __str__(self):
        return f"{self.user.username} - {self.rol}"

# Modelo para Herramientas
class Herramienta(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    estado = models.CharField(max_length=50, choices=[
        ('disponible', 'Disponible'),
        ('asignada', 'Asignada'),
        ('en_mantenimiento', 'En Mantenimiento'),
        ('fuera_de_servicio', 'Fuera de Servicio'),
    ], default='disponible')
    empleado = models.ForeignKey(Empleado, on_delete=models.SET_NULL, null=True, blank=True, related_name='herramientas')
    fecha_asignacion = models.DateField(null=True, blank=True)
    fecha_devolucion = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} ({self.estado})"