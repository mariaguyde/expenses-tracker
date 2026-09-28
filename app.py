from flask import Flask, render_template, request, jsonify, json, redirect, url_for

app = Flask(__name__)

@app.route("/")
def home():

    with open("data/categories.json", "r", encoding="utf-8") as f:
        categories = json.load(f)

    return render_template('index.html',categories=categories);

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

    #return jsonify({"success": True, "expense": expense, "amount": amount, "date": date})
    return redirect(url_for('home'))


app.run(debug=True)
