from flask import send_file
from io import BytesIO

import json
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from datetime import datetime
from utils import getDateInDDMMYYYY
from storage import getCategoryName

def generatepdf(filter_data):
    pdf_buffer = BytesIO()
    
    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter,rightMargin=50, leftMargin=50, topMargin=50, bottomMargin=50)
    style_title = ParagraphStyle('Title', fontSize=18, bold=True, alignment=1);
    elements = [Paragraph('Expenses Report', style_title), Spacer(1, 40)];
    
    # Table
    styles = getSampleStyleSheet()
    style_text = styles['Normal']
    style_cell = ParagraphStyle('Cell', parent=style_text, fontSize=11, leading=12)
    style_header = ParagraphStyle('Header', fontSize=12, leading=13)
    dataTable = [[Paragraph("<b>Name</b>", style_header), Paragraph("<b>Amount</b>", style_header), Paragraph("<b>Category</b>", style_header), Paragraph("<b>Date</b>", style_header), Paragraph("<b>Notes</b>", style_header)]];
    
    with open("data/data.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    if filter_data:
        data["expenses"] = [e for e in data["expenses"] if filter_data["start"] <= e["date"] <= filter_data["end"]]
        style_period = ParagraphStyle('Period', fontSize=12, leading=12)
        period = getDateInDDMMYYYY(filter_data["start"]) + " - " + getDateInDDMMYYYY(filter_data["end"])
        elements.append(Paragraph(period, style_period))
        elements.append(Spacer(1, 20))

    for expense in data["expenses"]:
        expense["date"] = datetime.strptime(expense["date"], "%Y-%m-%d").strftime("%d/%m/%Y")
        dataTable.append([
            Paragraph(expense["expense"], style_cell),
            Paragraph(expense["amount"], style_cell),
            Paragraph(getCategoryName(expense["category"]), style_cell),
            Paragraph(expense["date"], style_cell),
            Paragraph(expense["notes"] if "notes" in expense else "", style_cell)
        ])
    
    colWidthPersonalized = [150, 70, 100, 90, 100];
    table = Table(dataTable, colWidths=colWidthPersonalized)
    table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING',  (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING',    (0, 0), (-1, -1), 7.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 7.5),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#ababad")),
    ]))
    
    elements.append(table)
    doc.build(elements)
    pdf_buffer.seek(0)
    return pdf_buffer