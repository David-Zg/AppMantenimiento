from django.db import models

class InformeMantenimiento(models.Model):
    TIPO_MANTENIMIENTO = [
        ('preventivo', 'Preventivo'),
        ('correctivo', 'Correctivo'),
        ('predictivo', 'Predictivo'),
    ]
    
    # Campos existentes
    equipo = models.CharField(max_length=200)
    numero_serie = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=200)
    tipo_mantenimiento = models.CharField(max_length=20, choices=TIPO_MANTENIMIENTO)
    fecha_mantenimiento = models.DateField()
    tecnico = models.CharField(max_length=100)
    descripcion_trabajo = models.TextField()
    materiales_utilizados = models.TextField(blank=True)
    observaciones = models.TextField(blank=True)
    proximo_mantenimiento = models.DateField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    # Nuevos campos para el formato específico
    cliente = models.CharField(max_length=200)
    direccion = models.TextField()
    orden_trabajo = models.CharField(max_length=50)
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    identificacion = models.CharField(max_length=100)
    procedencia = models.CharField(max_length=100)
    frecuencia = models.CharField(max_length=50)
    alcance = models.CharField(max_length=100)
    tension = models.CharField(max_length=50)
    division = models.CharField(max_length=50)
    intensidad = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.equipo} - {self.fecha_mantenimiento}"