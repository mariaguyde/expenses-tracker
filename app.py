from flask import Flask, render_template, request, jsonify, json, redirect, url_for

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from flask import send_file
from io import BytesIO

app = Flask(__name__)

@app.route("/")
def home():

    with open("data/categories.json", "r", encoding="utf-8") as f:
        categories = json.load(f)

    with open("data/data.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    return render_template('index.html',categories=categories, expenses=data["expenses"]);

@app.route("/add", methods=["POST"])
def add():

    expense = request.form["expense"]
    amount = request.form["amount"]
    date = request.form["date"]
    category = request.form["category"]

    with open("data/data.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    data["expenses"].append({
        "expense": expense,
        "amount": amount,
        "date": date,
        "category": category
    })

    with open("data/data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    return jsonify({"date": date, "amount": amount, "expense": expense})
    #return redirect(url_for('home'))


@app.route("/download")
def download():
    pdf_data = generatepdf()
    
    return send_file(
        pdf_data,
        mimetype='application/pdf',
        as_attachment=True,             
        download_name='rapport_budget.pdf'
    )   


def generatepdf():
    pdf_buffer = BytesIO()
    
    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter,rightMargin=20, leftMargin=20, topMargin=20, bottomMargin=20)
    elements = [ Spacer(1, 12),Paragraph('Expenses Report'), Spacer(1, 12)];
    
    # Table
    styles = getSampleStyleSheet()
    style_text = styles['Normal']
    style_cell = ParagraphStyle('Cell', parent=style_text, fontSize=10, leading=12)
    style_header = ParagraphStyle('Header', parent=style_text, fontSize=11, leading=13, textColor=colors.whitesmoke)
    dataTable = [[Paragraph("<b>Name</b>", style_header), Paragraph("<b>Amount</b>", style_header), Paragraph("<b>Category</b>", style_header), Paragraph("<b>Date</b>", style_header)]];
    
    with open("data/data.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    for expense in data["expenses"]:
        dataTable.append([
            Paragraph(expense["expense"], style_cell),
            Paragraph(expense["amount"], style_cell),
            Paragraph(getCategoryName(expense["category"]), style_cell),
            Paragraph(expense["date"], style_cell)
        ])
    
    colWidthPersonalized = [150, 100, 100, 100];
    tableau = Table(dataTable, colWidths=colWidthPersonalized)
    tableau.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1A365D")),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F7FAFC")]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
    ]))
    
    elements.append(tableau)
    doc.build(elements)
    pdf_buffer.seek(0)
    return pdf_buffer

def getCategoryName(category_id):
    with open("data/categories.json", "r", encoding="utf-8") as f:
        categories = json.load(f)

    for category in categories:
        if int(category["id"]) == int(category_id):
            return category["name"]
    return "Unknown"

app.run(debug=True)
