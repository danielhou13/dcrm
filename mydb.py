import mysql.connector

# Change credentials to your own database credentials as required
dataBase = mysql.connector.connect(host="localhost", user="root", passwd="test")

cursorObject = dataBase.cursor()

# create database
cursorObject.execute("CREATE DATABASE elderco")
