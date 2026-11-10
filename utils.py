from datetime import datetime

def getDateInDDMMYYYY(date):
    return datetime.strptime(date, "%Y-%m-%d").strftime("%d/%m/%Y")