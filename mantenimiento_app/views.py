from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import InformeMantenimientoForm
from .pdf_utils import generar_pdf_informe

def formulario_mantenimiento(request):
    if request.method == 'POST':
        form = InformeMantenimientoForm(request.POST)
        if form.is_valid():
            informe = form.save()
            return redirect('mantenimiento_app:confirmacion', informe_id=informe.id)
    else:
        form = InformeMantenimientoForm()
    
    return render(request, 'mantenimiento_app/formulario.html', {'form': form})

def confirmacion(request, informe_id):
    from .models import InformeMantenimiento
    try:
        informe = InformeMantenimiento.objects.get(id=informe_id)
        return render(request, 'mantenimiento_app/confirmacion.html', {'informe': informe})
    except InformeMantenimiento.DoesNotExist:
        return HttpResponse("Informe no encontrado")

def descargar_pdf(request, informe_id):
    from .models import InformeMantenimiento
    try:
        informe = InformeMantenimiento.objects.get(id=informe_id)
        
        response = HttpResponse(content_type='application/pdf')
        filename = f"informe_mantenimiento_{informe.equipo.replace(' ', '_')}_{informe.fecha_mantenimiento}.pdf"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        pdf = generar_pdf_informe(informe)
        response.write(pdf)
        
        return response
        
    except InformeMantenimiento.DoesNotExist:
        return HttpResponse("Informe no encontrado")