import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="12345678Aa",
  database="Online_Bookstore_Project_Seden_Canpolat"
)

mycursor = mydb.cursor()

mycursor.execute("USE Online_Bookstore_Project_Seden_Canpolat")

