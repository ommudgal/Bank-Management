import mysql.connector
import os
from flask import Flask, request, redirect, url_for, render_template
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


class Mysql:
    mydb = mysql.connector.connect(
        host="localhost",
        user=os.getenv("mysql_user"),
        password=os.getenv("mysql_password"),
        database=os.getenv("mysql_database"),
    )
    cursor = mydb.cursor()


def check_account_exists(email):
    Mysql.cursor.execute(f"SELECT * FROM users WHERE email = '{email}'")
    result = Mysql.cursor.fetchall()
    if result:
        return True
    return False
