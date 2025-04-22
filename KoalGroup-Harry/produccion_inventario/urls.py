# produccion_inventario/urls.py
from django.urls import path
from .views import RegistrarControlIngreso, ControlIngresoList, ActualizarControlIngreso, trabajadores_por_rol, herramientas_asignadas, completar_perfil
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', ControlIngresoList.as_view(), name='control_ingreso_list'),
    path('control-ingreso/nuevo/', RegistrarControlIngreso.as_view(), name='control_ingreso_create'),
    path('control-ingreso/<int:pk>/editar/', ActualizarControlIngreso.as_view(), name='control_ingreso_update'),
    path('trabajadores-por-rol/', trabajadores_por_rol, name='trabajadores_por_rol'),
    path('herramientas-asignadas/', herramientas_asignadas, name='herramientas_asignadas'),
    path('completar-perfil/', completar_perfil, name='completar_perfil'),
    path('login/', LoginView.as_view(template_name='produccion_inventario/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login', http_method_names=['get', 'post']), name='logout'),
]