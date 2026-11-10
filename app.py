from flask import Flask, render_template, request, jsonify, json, redirect, url_for, send_file
from datetime import datetime

from pdf_report import generatepdf
from utils import  getDateInDDMMYYYY
from storage import getAllCategories, getAllExpenses, addExpense, deleteExpense, getCategoryName

app = Flask(__name__)
app.json.sort_keys = False

@app.route("/")
def home():
    return render_template('index.html',categories=getAllCategories(), expenses=getAllExpenses());

@app.route("/add", methods=["POST"])
def add():
    result = addExpense(request.form)
    return jsonify(result)

@app.route("/delete/<id>", methods=["POST"])
def delete(id):
    result = deleteExpense(id)
    return jsonify(result)


@app.route("/download", methods=["GET"])
def download():

    filter_data = False;
    if request.args.get('date-start') and request.args.get('date-end'):
        filter_data = {"start": request.args.get('date-start'), "end": request.args.get('date-end')};

    pdf_data = generatepdf(filter_data)

    return send_file(
        pdf_data,
        mimetype='application/pdf',
        as_attachment=True,             
        download_name='expenses_report.pdf'
    )   


app.run(debug=True)
