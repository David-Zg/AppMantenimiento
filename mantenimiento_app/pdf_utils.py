from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib import colors
from reportlab.lib.units import inch, cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from django.conf import settings
import os
from datetime import datetime

def generar_pdf_informe(informe):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=1*cm, bottomMargin=1*cm)
    styles = getSampleStyleSheet()
    story = []
    
    # Estilos personalizados
    styles.add(ParagraphStyle(
        name='Header1',
        parent=styles['Heading1'],
        fontSize=14,
        textColor=colors.black,
        spaceAfter=12,
        alignment=1  # Centrado
    ))
    
    styles.add(ParagraphStyle(
        name='Header2',
        parent=styles['Heading2'],
        fontSize=12,
        textColor=colors.black,
        spaceAfter=6,
        alignment=0  # Izquierda
    ))
    
    styles.add(ParagraphStyle(
        name='NormalBold',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.black,
        spaceAfter=6,
        alignment=0
    ))
    
    styles.add(ParagraphStyle(
        name='TableHeader',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.white,
        backColor=colors.HexColor('#2F5496'),
        alignment=1
    ))
    
    # ===== ENCABEZADO =====
    # Tabla de información del cliente
    datos_cliente = [
        [Paragraph("<b>CLIENTE</b>", styles['NormalBold']), 
         Paragraph(f": <b>{informe.cliente if hasattr(informe, 'cliente') else 'TECNOLÓGICA DE ALIMENTOS S.A.'}</b>", styles['NormalBold']), 
         "", ""],
        [Paragraph("<b>DIRECCIÓN</b>", styles['NormalBold']), 
         Paragraph(f": {informe.direccion if hasattr(informe, 'direccion') else 'Panamericana Sur km 61 Fnd. La Quipa (Lima/Lima/Pucusana)'}", styles['NormalBold']), 
         "", ""],
        [Paragraph("<b>INSTRUMENTO</b>", styles['NormalBold']), 
         Paragraph(f": <b>{informe.equipo}</b>", styles['NormalBold']), 
         "", ""],
        [Paragraph("<b>ORDEN DE TRABAJO</b>", styles['NormalBold']), 
         Paragraph(f": {informe.orden_trabajo if hasattr(informe, 'orden_trabajo') else 'OT-02502645'}", styles['NormalBold']), 
         Paragraph("<b>FECHA DE ATENCIÓN</b>", styles['NormalBold']), 
         Paragraph(f": {informe.fecha_mantenimiento.strftime('%Y/%m/%d')}", styles['NormalBold'])],
        [Paragraph("<b>UBICACIÓN</b>", styles['NormalBold']), 
         Paragraph(f": {informe.ubicacion}", styles['NormalBold']), 
         "", ""],
        [Paragraph("<b>TIPO DE SERVICIO</b>", styles['NormalBold']), 
         Paragraph(f": {informe.get_tipo_mantenimiento_display()}", styles['NormalBold']), 
         "", ""],
    ]
    
    tabla_cliente = Table(datos_cliente, colWidths=[1.5*inch, 3*inch, 1.5*inch, 1.5*inch])
    tabla_cliente.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#D9E2F3')),
        ('BACKGROUND', (0, 2), (-1, 2), colors.HexColor('#D9E2F3')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    
    story.append(tabla_cliente)
    story.append(Spacer(1, 0.3*inch))
    
    # ===== 1. DATOS TÉCNICOS =====
    story.append(Paragraph("<u>1. DATOS TÉCNICOS:</u>", styles['Header2']))
    
    datos_tecnicos = [
        [Paragraph("<b>Marca</b>", styles['NormalBold']), 
         Paragraph(f": {informe.marca if hasattr(informe, 'marca') else 'JULABO'}", styles['Normal']),
         Paragraph("<b>Identificación</b>", styles['NormalBold']), 
         Paragraph(f": {informe.identificacion if hasattr(informe, 'identificacion') else 'CHI-002'}", styles['Normal'])],
        
        [Paragraph("<b>Modelo</b>", styles['NormalBold']), 
         Paragraph(f": {informe.modelo if hasattr(informe, 'modelo') else 'F12 - EH'}", styles['Normal']),
         Paragraph("<b>Procedencia</b>", styles['NormalBold']), 
         Paragraph(f": {informe.procedencia if hasattr(informe, 'procedencia') else 'Alemania'}", styles['Normal'])],
        
        [Paragraph("<b>Nº de serie</b>", styles['NormalBold']), 
         Paragraph(f": {informe.numero_serie}", styles['Normal']),
         Paragraph("<b>Frecuencia</b>", styles['NormalBold']), 
         Paragraph(f": {informe.frecuencia if hasattr(informe, 'frecuencia') else '60 Hz'}", styles['Normal'])],
        
        [Paragraph("<b>Alcance de escala de medición</b>", styles['NormalBold']), 
         Paragraph(f": {informe.alcance if hasattr(informe, 'alcance') else '-20,0 °C a 150,0 °C'}", styles['Normal']),
         Paragraph("<b>Tensión</b>", styles['NormalBold']), 
         Paragraph(f": {informe.tension if hasattr(informe, 'tension') else '230 v'}", styles['Normal'])],
        
        [Paragraph("<b>División de escala de medición</b>", styles['NormalBold']), 
         Paragraph(f": {informe.division if hasattr(informe, 'division') else '0,1 °C'}", styles['Normal']),
         Paragraph("<b>Intensidad</b>", styles['NormalBold']), 
         Paragraph(f": {informe.intensidad if hasattr(informe, 'intensidad') else 'No indica'}", styles['Normal'])],
    ]
    
    tabla_tecnicos = Table(datos_tecnicos, colWidths=[2*inch, 2*inch, 1.5*inch, 1.5*inch])
    tabla_tecnicos.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('PADDING', (0, 0), (-1, -1), 4),
    ]))
    
    story.append(tabla_tecnicos)
    story.append(Spacer(1, 0.2*inch))
    
    # ===== 2. CONDICIONES INICIALES =====
    story.append(Paragraph("<u>2. CONDICIONES INICIALES:</u>", styles['Header2']))
    
    condiciones = [
        "• El equipo se encontró operativo.",
        "• Se observa polvo, grasa en la carcasa del equipo.",
        "• Hélices del motor obstruidas.",
        "• No se observa completo la indicación en el display (leds de indicación incompletos)"
    ]
    
    for condicion in condiciones:
        story.append(Paragraph(condicion, styles['Normal']))
        story.append(Spacer(1, 0.05*inch))
    
    story.append(Spacer(1, 0.1*inch))
    
    # ===== 3. TRABAJO REALIZADO =====
    story.append(Paragraph("<u>3. TRABAJO REALIZADO:</u>", styles['Header2']))
    
    trabajos = [
        "• Inspección física conforme.",
        "• Revisión de los parámetros de configuración.",
        "• Desmontaje del equipo.",
        "• Limpieza interna de la zona de trabajo.",
        "• Limpieza del sistema de refrigeración (compresor y accesorios).",
        "• Limpieza de la resistencia de calentamiento, sistema de circulación.",
        "• Limpieza de tarjeta y dispositivos electrónicos.",
        "• Cableado interno conforme.",
        "• Sensor de temperatura conforme.",
        "• Montaje del equipo.",
        "• Pruebas de funcionamiento en 0 °C ± 1 °C."
    ]
    
    for trabajo in trabajos:
        story.append(Paragraph(trabajo, styles['Normal']))
        story.append(Spacer(1, 0.05*inch))
    
    # Tabla de pruebas
    datos_pruebas = [
        [Paragraph("<b>VALOR SETEADO</b>", styles['TableHeader']), 
         Paragraph("<b>VALOR MÁXIMO DE INDICACION</b>", styles['TableHeader']), 
         Paragraph("<b>VALOR MÍNIMO DE INDICACIÓN</b>", styles['TableHeader'])],
        ["-1 °C", "0,04 °C", "-0,20 °C"]
    ]
    
    tabla_pruebas = Table(datos_pruebas, colWidths=[2*inch, 2.5*inch, 2.5*inch])
    tabla_pruebas.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2F5496')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    
    story.append(Spacer(1, 0.1*inch))
    story.append(tabla_pruebas)
    story.append(Spacer(1, 0.2*inch))
    
    # ===== 4. CONCLUSIONES =====
    story.append(Paragraph("<u>4. CONCLUSIONES:</u>", styles['Header2']))
    
    conclusiones = [
        "• El equipo queda operativo y funcionando.",
        "• Programar el equipo a -1 °C para obtener 0 °C ± 1 °C."
    ]
    
    for conclusion in conclusiones:
        story.append(Paragraph(conclusion, styles['Normal']))
        story.append(Spacer(1, 0.05*inch))
    
    story.append(Spacer(1, 0.1*inch))
    
    # ===== 5. OBSERVACIONES Y RECOMENDACIONES =====
    story.append(Paragraph("<u>5. OBSERVACIONES Y RECOMENDACIONES:</u>", styles['Header2']))
    
    observaciones = [
        "• Respetar las indicaciones del manual del fabricante.",
        "• Evite derramar sustancias ajenas al liquido de trabajo.",
        "• Retirar cualquier objeto o partícula extraña en la zona de trabajo."
    ]
    
    for observacion in observaciones:
        story.append(Paragraph(observacion, styles['Normal']))
        story.append(Spacer(1, 0.05*inch))
    
    story.append(Spacer(1, 0.3*inch))
    
    # ===== FIRMA =====
    firma_texto = "Sherman Arbildo Pinedo<br/><b>Responsable Técnico</b><br/>KOSSODO METROLOGIA S.A.C."
    story.append(Paragraph(firma_texto, styles['NormalBold']))
    
    doc.build(story)
    pdf = buffer.getvalue()
    buffer.close()
    return pdf