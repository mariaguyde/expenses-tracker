from flask import Flask, render_template, request, jsonify, json, redirect, url_for
from datetime import datetime

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from flask import send_file
from io import BytesIO

app = Flask(__name__)
app.json.sort_keys = False

@app.route("/")
def home():

    with open("data/categories.json", "r", encoding="utf-8") as f:
        categories = json.load(f)

    with open("data/data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    for e in data["expenses"]:
        e["category"] = getCategoryName(e["category"])
        e["date"] = datetime.strptime(e["date"], "%Y-%m-%d").strftime("%d/%m/%Y")

    return render_template('index.html',categories=categories, expenses=data["expenses"]);

@app.route("/add", methods=["POST"])
def add():

    expense = request.form["expense"]
    amount = request.form["amount"]
    date = request.form["date"]
    category = request.form["category"]
    notes = request.form["notes"]

    with open("data/data.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    id = str(len(data["expenses"]))
    data["expenses"].append({
        "id": id,
        "expense": expense,
        "amount": amount,
        "date": date,
        "category": category,
        "notes": notes
    })

    with open("data/data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    return jsonify({"expense": expense, "amount": amount,"category": getCategoryName(category), "date": getDateInDDMMYYYY(date), "notes": notes, "actions": id})

@app.route("/delete/<id>", methods=["POST"])
def delete(id):
    with open("data/data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    data["expenses"] = [e for e in data["expenses"] if e["id"] != id]
    with open("data/data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    return {"status": "ok"};


@app.route("/download")
def download():
    pdf_data = generatepdf()
    
    return send_file(
        pdf_data,
        mimetype='application/pdf',
        as_attachment=True,             
        download_name='expenses_report.pdf'
    )   


def generatepdf():
    pdf_buffer = BytesIO()
    
    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter,rightMargin=50, leftMargin=50, topMargin=50, bottomMargin=50)
    style_title = ParagraphStyle('Title', fontSize=18, bold=True, alignment=1);
    elements = [Paragraph('Expenses Report', style_title), Spacer(1, 40)];
    
    # Table
    styles = getSampleStyleSheet()
    style_text = styles['Normal']
    style_cell = ParagraphStyle('Cell', parent=style_text, fontSize=12, leading=12)
    style_header = ParagraphStyle('Header', parent=style_text, fontSize=12, leading=13, textColor=colors.black, bold=False)
    dataTable = [[Paragraph("<b>Name</b>", style_header), Paragraph("<b>Amount</b>", style_header), Paragraph("<b>Category</b>", style_header), Paragraph("<b>Date</b>", style_header), Paragraph("<b>Notes</b>", style_header)]];
    
    with open("data/data.json", "r", encoding="utf-8") as f:
        data = json.load(f)

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
    tableau = Table(dataTable, colWidths=colWidthPersonalized)
    tableau.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING',  (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING',    (0, 0), (-1, -1), 7.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 7.5),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#ababad")),
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

def getDateInDDMMYYYY(date):
    return datetime.strptime(date, "%Y-%m-%d").strftime("%d/%m/%Y")

app.run(debug=True)
