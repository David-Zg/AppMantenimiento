from django import forms
from .models import InformeMantenimiento

class InformeMantenimientoForm(forms.ModelForm):
    class Meta:
        model = InformeMantenimiento
        fields = '__all__'
        widgets = {
            'fecha_mantenimiento': forms.DateInput(attrs={'type': 'date'}),
            'proximo_mantenimiento': forms.DateInput(attrs={'type': 'date'}),
            'descripcion_trabajo': forms.Textarea(attrs={'rows': 4}),
            'materiales_utilizados': forms.Textarea(attrs={'rows': 3}),
            'observaciones': forms.Textarea(attrs={'rows': 3}),
            'direccion': forms.Textarea(attrs={'rows': 2}),
        }