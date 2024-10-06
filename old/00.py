import mysql.connector
import os
from dotenv import load_dotenv
from otpmaker import send_otp, generate_otp

load_dotenv()


class Mysql:
    mydb = mysql.connector.connect(
        host="localhost",
        user=os.getenv("mysql_user"),
        password=os.getenv("mysql_password"),
        database=os.getenv("mysql_database"),
    )
    cursor = mydb.cursor()


def check_account_exists(email):
    Mysql.cursor.execute(f"SELECT * FROM logdata WHERE email = '{email}'")
    result = Mysql.cursor.fetchall()
    if result:
        return True
    return False


while True:
    print(
        """Choose an option:
          1. Create account
          2. Login
          3. Exit"""
    )
    choice = input()
    if choice == "1":
        email = input("Enter email: ")
        if check_account_exists(email):
            print("Account already exists")
        else:
            password = input("Enter password: ")
            Mysql.cursor.execute(
                f"INSERT INTO logdata (email, password) VALUES ('{email}', '{password}')"
            )
            Mysql.cursor.execute(
                f"INSERT INTO balance (email, balance) VALUES ('{email}', 0)"
            )
            Mysql.mydb.commit()
            print("Account created successfully")
    elif choice == "2":
        email = input("Enter email: ")
        if not check_account_exists(email):
            print("Account does not exist")
        else:
            password = input("Enter password: ")
            Mysql.cursor.execute(
                f"SELECT * FROM logdata WHERE email = '{email}' AND password = '{password}'"
            )
            result = Mysql.cursor.fetchall()
            if result and result[0][0] == email and result[0][1] == password:
                print("Enter OTP sent to your email")
                otp = generate_otp()
                send_otp(email, otp)
                user_otp = input("Enter OTP: ")
                if otp != int(user_otp):
                    print("Invalid OTP")
                    continue
                print("Login successful")
            while True:
                print(
                    """Choose an option:
                  1. Check balance
                  2. Withdraw
                  3. Deposit
                  4. Exit"""
                )
                choice = input()
                if choice == "1":
                    Mysql.cursor.execute(
                        f"SELECT balance FROM balance WHERE email = '{email}'"
                    )
                    result = Mysql.cursor.fetchall()
                    print(f"Your balance is {result[0][0]}")
                elif choice == "2":
                    amount = int(input("Enter amount to withdraw: "))
                    Mysql.cursor.execute(
                        f"SELECT balance FROM balance WHERE email = '{email}'"
                    )
                    result = Mysql.cursor.fetchall()
                    balance = result[0][0]
                    if balance < amount:
                        print("Insufficient balance")
                    else:
                        balance -= amount
                        Mysql.cursor.execute(
                            f"UPDATE balance SET balance = {balance} WHERE email = '{email}'"
                        )
                        Mysql.mydb.commit()
                        print("Amount withdrawn successfully")
                elif choice == "3":
                    amount = int(input("Enter amount to deposit: "))
                    Mysql.cursor.execute(
                        f"SELECT balance FROM balance WHERE email = '{email}'"
                    )
                    result = Mysql.cursor.fetchall()
                    balance = result[0][0]
                    balance += amount
                    Mysql.cursor.execute(
                        f"UPDATE balance SET balance = {balance} WHERE email = '{email}'"
                    )
                    Mysql.mydb.commit()
                    print("Amount deposited successfully")
                elif choice == "4":
                    break
                else:
                    print("Invalid choice, please try again.")
            else:
                print("Invalid credentials")
    elif choice == "3":
        print("Exiting")
        break
    else:
        print("Invalid choice, please try again.")
