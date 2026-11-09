import json
from datetime import datetime

def getCategoryName(category_id):
    with open("data/categories.json", "r", encoding="utf-8") as f:
        categories = json.load(f)

    for category in categories:
        if int(category["id"]) == int(category_id):
            return category["name"]
    return "Unknown"

def getDateInDDMMYYYY(date):
    return datetime.strptime(date, "%Y-%m-%d").strftime("%d/%m/%Y")