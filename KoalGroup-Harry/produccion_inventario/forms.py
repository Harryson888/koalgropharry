# produccion_inventario/forms.py
from django import forms
from .models import Herramienta, Empleado

class AsignarHerramientaForm(forms.ModelForm):
    class Meta:
        model = Herramienta
        fields = ['empleado', 'fecha_asignacion', 'fecha_devolucion']
        widgets = {
            'fecha_asignacion': forms.DateInput(attrs={'type': 'date'}),
            'fecha_devolucion': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['empleado'].required = False
        self.fields['fecha_devolucion'].required = False

    def clean(self):
        cleaned_data = super().clean()
        empleado = cleaned_data.get('empleado')
        fecha_asignacion = cleaned_data.get('fecha_asignacion')
        fecha_devolucion = cleaned_data.get('fecha_devolucion')

        if empleado and not fecha_asignacion:
            self.add_error('fecha_asignacion', 'La fecha de asignación es obligatoria si se asigna un empleado.')
        if fecha_devolucion and fecha_asignacion and fecha_devolucion < fecha_asignacion:
            self.add_error('fecha_devolucion', 'La fecha de devolución no puede ser anterior a la fecha de asignación.')

class ActualizarEstadoHerramientaForm(forms.ModelForm):
    class Meta:
        model = Herramienta
        fields = ['estado']

class CrearHerramientaForm(forms.ModelForm):
    class Meta:
        model = Herramienta
        fields = ['nombre', 'descripcion', 'estado']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']
        if not nombre:
            raise forms.ValidationError('El nombre de la herramienta es obligatorio.')
        if Herramienta.objects.filter(nombre=nombre).exists():
            raise forms.ValidationError('Ya existe una herramienta con este nombre.')
        return nombre