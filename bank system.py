import sqlite3
import getpass
from tabulate import tabulate

# DB setup
conn = sqlite3.connect("bank.db")
cur = conn.cursor()

cur.execute('''
    CREATE TABLE IF NOT EXISTS accounts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        account_no TEXT UNIQUE NOT NULL,
        pin TEXT NOT NULL,
        balance REAL DEFAULT 0.0
    )
''')
conn.commit()

def register():
    print("\n--- New Account Registration ---")
    name = input("Enter your name: ")
    acc_no = input("Create your account number: ")
    pin = input("Set your 4-digit PIN: ")

    try:
        cur.execute("INSERT INTO accounts (name, account_no, pin) VALUES (?, ?, ?)", (name, acc_no, pin))
        conn.commit()
        print("✅ Account created successfully!\n")
    except sqlite3.IntegrityError:
        print("❌ Account number already exists. Try again.")

def login():
    print("\n--- Login ---")
    acc_no = input("Enter account number: ")
    pin = getpass.getpass("Enter 4-digit PIN: ")

    cur.execute("SELECT * FROM accounts WHERE account_no=? AND pin=?", (acc_no, pin))
    user = cur.fetchone()

    if user:
        print(f"\n🎉 Welcome {user[1]}!")
        return user
    else:
        print("❌ Invalid credentials.")
        return None

def atm_menu(user):
    while True:
        print("\n--- ATM Menu ---")
        print("1. Balance Inquiry\n2. Deposit\n3. Withdraw\n4. Change PIN\n5. Logout")
        choice = input("Select an option: ")

        if choice == '1':
            cur.execute("SELECT balance FROM accounts WHERE account_no=?", (user[2],))
            balance = cur.fetchone()[0]
            print(f"💰 Current Balance: ₹{balance}")
        
        elif choice == '2':
            amount = float(input("Enter deposit amount: "))
            cur.execute("UPDATE accounts SET balance = balance + ? WHERE account_no=?", (amount, user[2]))
            conn.commit()
            print("✅ Amount deposited!")

        elif choice == '3':
            amount = float(input("Enter withdrawal amount: "))
            cur.execute("SELECT balance FROM accounts WHERE account_no=?", (user[2],))
            balance = cur.fetchone()[0]

            if amount > balance:
                print("❌ Insufficient balance.")
            else:
                cur.execute("UPDATE accounts SET balance = balance - ? WHERE account_no=?", (amount, user[2]))
                conn.commit()
                print("✅ Withdrawal successful!")

        elif choice == '4':
            new_pin = input("Enter new 4-digit PIN: ")
            cur.execute("UPDATE accounts SET pin=? WHERE account_no=?", (new_pin, user[2]))
            conn.commit()
            print("🔑 PIN changed successfully.")

        elif choice == '5':
            print("👋 Logged out.")
            break
        else:
            print("❗ Invalid option. Try again.")

def view_users():  # Admin feature (optional)
    cur.execute("SELECT id, name, account_no, balance FROM accounts")
    users = cur.fetchall()
    print("\n--- User Accounts ---")
    print(tabulate(users, headers=["ID", "Name", "Account No", "Balance"], tablefmt="fancy_grid"))

def main():
    while True:
        print("\n====== MINI BANKING SYSTEM ======")
        print("1. Register")
        print("2. Login")
        print("3. View All Accounts (Admin)")
        print("4. Exit")
        ch = input("Choose an option: ")

        if ch == '1':
            register()
        elif ch == '2':
            user = login()
            if user:
                atm_menu(user)
        elif ch == '3':
            view_users()
        elif ch == '4':
            print("🏁 Exiting system. Goodbye!")
            break
        else:
            print("❌ Invalid choice.")

main()
conn.close()
