import sqlite3
conn = sqlite3.connect('ClientInformation.db')
curs = conn.cursor()

VAT = 1.2

sql = "SELECT FROM TreatmentPrice
