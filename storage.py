import json, uuid
from datetime import datetime
from utils import getCategoryName, getDateInDDMMYYYY

def getAllCategories():
    with open("data/categories.json", "r", encoding="utf-8") as f:
        categories = json.load(f)
    return categories

def getAllExpenses():
    with open("data/data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    for e in data["expenses"]:
        e["category"] = getCategoryName(e["category"])
        e["date"] = getDateInDDMMYYYY(e["date"])
    return data["expenses"]

def addExpense(data):
    expense = data["expense"]
    amount = data["amount"]
    date = data["date"]
    category = data["category"]
    notes = data["notes"]

    with open("data/data.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    id = uuid.uuid4().hex
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

    if id not in [e["id"] for e in data["expenses"]]:
        return False
    return {"expense": expense, "amount": amount,"category": getCategoryName(category), "date": getDateInDDMMYYYY(date), "notes": notes, "actions": id}

def deleteExpense(id):
    with open("data/data.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    data["expenses"] = [e for e in data["expenses"] if e["id"] != id]
    with open("data/data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    if id not in [e["id"] for e in data["expenses"]]:
        return True
    return False
