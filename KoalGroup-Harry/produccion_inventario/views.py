# produccion_inventario/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.db import models
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Proyecto, ControlIngreso, Empleado, Verificacion, ListaChequeo, Herramienta, UserProfile
from .forms import AsignarHerramientaForm, ActualizarEstadoHerramientaForm, CrearHerramientaForm

# Vista para listar controles de ingreso
class ControlIngresoList(LoginRequiredMixin, ListView):
    model = ControlIngreso
    template_name = 'produccion_inventario/control_ingreso_list.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        return ControlIngreso.objects.select_related('proyecto').all()

# Vista para registrar un nuevo control de ingreso
class RegistrarControlIngreso(LoginRequiredMixin, CreateView):
    model = ControlIngreso
    fields = ['fecha', 'cantidad', 'proyecto']
    template_name = 'produccion_inventario/control_ingreso_form.html'
    success_url = reverse_lazy('control_ingreso_list')

    def form_valid(self, form):
        messages.success(self.request, 'Control de ingreso registrado correctamente.')
        return super().form_valid(form)

# Vista para actualizar un control de ingreso existente
class ActualizarControlIngreso(LoginRequiredMixin, UpdateView):
    model = ControlIngreso
    fields = ['fecha', 'cantidad', 'proyecto']
    template_name = 'produccion_inventario/control_ingreso_form.html'
    success_url = reverse_lazy('control_ingreso_list')

    def form_valid(self, form):
        messages.success(self.request, 'Control de ingreso actualizado correctamente.')
        return super().form_valid(form)

# Vista para completar el perfil del usuario
@login_required
def completar_perfil(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
        messages.info(request, 'Ya tienes un perfil asociado.')
        return redirect('control_ingreso_list')
    except UserProfile.DoesNotExist:
        if request.method == 'POST':
            rol = request.POST.get('rol')
            if rol in ['supervisor', 'trabajador']:
                UserProfile.objects.create(user=request.user, rol=rol)
                messages.success(request, 'Perfil creado correctamente.')
                return redirect('control_ingreso_list')
            else:
                messages.error(request, 'Por favor, selecciona un rol válido.')
        return render(request, 'produccion_inventario/completar_perfil.html', {})

# RF3: Mostrar trabajadores por rol (solo para supervisores)
@login_required
def trabajadores_por_rol(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        return redirect('completar_perfil')

    if profile.rol != 'supervisor':
        messages.error(request, 'No tienes permisos para acceder a esta página. Debes ser un supervisor.')
        return redirect('control_ingreso_list')

    roles = Empleado.objects.values('rol').distinct()
    trabajadores = {}
    for rol in roles:
        rol_name = rol['rol']
        trabajadores[rol_name] = Empleado.objects.filter(rol=rol_name)
    return render(request, 'produccion_inventario/trabajadores_por_rol.html', {'trabajadores': trabajadores})

# RF4 y RF5: Mostrar herramientas asignadas y su estado (solo para supervisores)
@login_required
def herramientas_asignadas(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        return redirect('completar_perfil')

    if profile.rol != 'supervisor':
        messages.error(request, 'No tienes permisos para acceder a esta página. Debes ser un supervisor.')
        return redirect('control_ingreso_list')

    herramientas = Herramienta.objects.all().select_related('empleado')
    empleados = Empleado.objects.all()
    estado_choices = Herramienta._meta.get_field('estado').choices
    estado_filtro = request.GET.get('estado', '')
    empleado_filtro = request.GET.get('empleado', '')
    if estado_filtro:
        herramientas = herramientas.filter(estado=estado_filtro)
    if empleado_filtro:
        herramientas = herramientas.filter(empleado_id=empleado_filtro)
    paginator = Paginator(herramientas, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    crear_herramienta_form = CrearHerramientaForm()
    if request.method == 'POST':
        action = request.POST.get('action')
        herramienta_id = request.POST.get('herramienta_id')
        if action == 'crear_herramienta':
            crear_herramienta_form = CrearHerramientaForm(request.POST)
            if crear_herramienta_form.is_valid():
                crear_herramienta_form.save()
                messages.success(request, 'Herramienta creada correctamente.')
                return redirect('herramientas_asignadas')
            else:
                messages.error(request, 'Error al crear la herramienta. Verifica los datos.')
        elif action == 'asignar':
            herramienta = get_object_or_404(Herramienta, id=herramienta_id)
            form = AsignarHerramientaForm(request.POST, instance=herramienta)
            if form.is_valid():
                if not form.cleaned_data['empleado']:
                    herramienta.fecha_asignacion = None
                    herramienta.fecha_devolucion = None
                    herramienta.estado = 'disponible'
                else:
                    herramienta.estado = 'asignada'
                form.save()
                messages.success(request, f'Herramienta "{herramienta.nombre}" actualizada correctamente.')
            else:
                messages.error(request, 'Error al asignar/desasignar la herramienta. Verifica los datos.')
        elif action == 'actualizar_estado':
            herramienta = get_object_or_404(Herramienta, id=herramienta_id)
            form = ActualizarEstadoHerramientaForm(request.POST, instance=herramienta)
            if form.is_valid():
                form.save()
                messages.success(request, f'Estado de la herramienta "{herramienta.nombre}" actualizado correctamente.')
            else:
                messages.error(request, 'Error al actualizar el estado de la herramienta.')
        return redirect('herramientas_asignadas')
    return render(request, 'produccion_inventario/herramientas_asignadas.html', {
        'herramientas': page_obj,
        'empleados': empleados,
        'estado_choices': estado_choices,
        'estado_filtro': estado_filtro,
        'empleado_filtro': empleado_filtro,
        'crear_herramienta_form': crear_herramienta_form,
    })