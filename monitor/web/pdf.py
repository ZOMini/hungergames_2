import datetime
import io

from flask import make_response, request
from reportlab.lib.pagesizes import landscape, letter
from reportlab.pdfgen import canvas


def post_download_pdf():
    """Формирует ответ с pdf файлом."""
    buffer = io.BytesIO()
    report = canvas.Canvas(buffer, pagesize=landscape(letter), initialFontSize=8)
    for n, line in enumerate(request.form['logs'].strip('[]}').split(', ')):
        report.drawString(10 , 550 - (n * 14), line)
    report.saveState()
    report.save()
    pdf = buffer.getvalue()
    buffer.close()
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=logs_{datetime.datetime.now()}.pdf'
    return response
