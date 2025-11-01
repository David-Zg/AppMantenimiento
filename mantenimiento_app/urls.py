from django.urls import path
from . import views

app_name = 'mantenimiento_app'

urlpatterns = [
    path('', views.formulario_mantenimiento, name='formulario'),
    path('confirmacion/<int:informe_id>/', views.confirmacion, name='confirmacion'),
    path('descargar-pdf/<int:informe_id>/', views.descargar_pdf, name='descargar_pdf'),
]