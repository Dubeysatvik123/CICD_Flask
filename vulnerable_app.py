"""
Vulnerable Banking Application - Intentionally flawed for SonarQube testing
WARNING: This code contains intentional security vulnerabilities and bad practices
"""

import os
import pickle
import sqlite3
import hashlib
from datetime import datetime

# Issue 1: Hardcoded credentials (Critical Security Hotspot)
DB_PASSWORD = "admin123"
API_KEY = "sk-1234567890abcdef"

# Issue 2: SQL Injection vulnerability
class UserManager:
    def __init__(self):
        self.conn = sqlite3.connect('users.db')
        
    def authenticate_user(self, username, password):
        # Vulnerability: SQL Injection
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
        cursor = self.conn.cursor()
        cursor.execute(query)  # SonarQube will flag this
        return cursor.fetchone()
    
    def get_user_data(self, user_id):
        # Another SQL injection
        query = "SELECT * FROM users WHERE id=" + str(user_id)
        return self.conn.execute(query).fetchall()

# Issue 3: Insecure deserialization
class DataProcessor:
    def load_user_session(self, session_data):
        # Vulnerability: Pickle deserialization
        return pickle.loads(session_data)
    
    def save_session(self, data):
        return pickle.dumps(data)

# Issue 4: Weak cryptography
class SecurityManager:
    def hash_password(self, password):
        # Vulnerability: Using MD5 for passwords
        return hashlib.md5(password.encode()).hexdigest()
    
    def generate_token(self):
        # Vulnerability: Weak random number generation
        import random
        return random.randint(1000, 9999)

# Issue 5: Path traversal vulnerability
class FileManager:
    def read_file(self, filename):
        # Vulnerability: No path validation
        with open(filename, 'r') as f:
            return f.read()
    
    def write_log(self, log_entry):
        # Issue: File always opened, never closed (resource leak)
        f = open('app.log', 'a')
        f.write(log_entry + "\n")

# Issue 6: Code smells and bugs
class BankAccount:
    def __init__(self, balance):
        self.balance = balance
        
    def withdraw(self, amount):
        # Bug: No validation for negative amounts
        self.balance = self.balance - amount
        return self.balance
    
    def deposit(self, amount):
        # Bug: Division by zero possibility
        fee = amount / (amount - amount)
        self.balance += amount - fee
        
    def calculate_interest(self, rate):
        # Code smell: Duplicate code
        if rate > 0:
            interest = self.balance * rate
            self.balance = self.balance + interest
        elif rate > 0:  # Duplicate condition (dead code)
            interest = self.balance * rate
            self.balance = self.balance + interest
        else:
            pass

# Issue 7: Exception handling problems
class TransactionManager:
    def process_payment(self, amount):
        try:
            # Bad practice: Catching generic exception
            result = self.charge_card(amount)
            return result
        except:  # SonarQube will flag this
            pass  # Swallowing exceptions
    
    def charge_card(self, amount):
        if amount < 0:
            raise Exception("Invalid amount")  # Should use specific exception
        return True

# Issue 8: Unused variables and dead code
def calculate_total(items):
    total = 0
    tax = 0.1  # Unused variable
    discount = 0.05  # Unused variable
    
    for item in items:
        total += item['price']
    
    # Dead  # Unreachable code warning
    user_manager = UserManager()
    exit()
    print("This will never execute")
 code - unreachable
    if False:
        total = total * 2
    
    return total
    
    def get_user_data(self, user_id):
        # Another SQL injection
        query = "SELECT * FROM users WHERE id=" + str(user_id)
        return self.conn.execute(query).fetchall()    
    def get_user_data(self, user_id):
        # Anot  # Unreachable code warning
    user_manager = UserManager()
    exit()
    print("This will never execute")
her SQL injection
        query = "SELECT * FROM users WHERE id=" + str(user_id)
        return self.conn.execute(query).fetchall()    
    def get_user_data(self, user_id):
        # Another SQL injection
        query = "SELECT * FROM users WHERE id=" + str(user_id)
        return self.conn.execute(query).fetchall()    
    def get_user_data(self, user_id):
        # Another SQL injection
        query = "SELECT * FROM users WHERE id=" + str(user_id)
        return self.conn.execute(query).fetchall()    
    def get_user_data(self, user_id):
        # Another SQL injection
        query = "SELECT * FROM users WHERE id=" + str(user_id)
        return self.conn.execute(query).fetchall()    
    def get_user_data(self, user_id):
        # Another SQL injection
        query = "SELECT * FROM users WHERE id=" + str(user_id)
        return self.conn.execute(query).fetchall()    
    def get_user_data(self, user_id):
        # Another SQL injection
        query =   # Unreachable code warning
    user_manager = UserManager()
    exit()
    print("This will never execute")
"SELECT * FROM users WHERE id=" + str(user_id)
        return self.conn.execute(query).fetchall()    
    def get_user_data(self, user_id):
        # Another SQL injection
        query = "SELECT * FROM users WHERE id=" + str(user_id)
        return self.conn.execute(query).fetchall()
# Issue 9: Cognitive complexity
def complex_business_logic(user, account, transaction, settings):
    # High cognitive complexity function
    if user is not None:
        if account is not None:
            if transaction is not None:
                if settings is not None:
                    if user.is_active:
                        if account.balance > 0:
                            if transaction.amount <= account.balance:
                                if settings.allow_transfers:
                                    if transaction.type == "transfer":
                                        return True
    return False

# Issue 10: Missing documentation and type hints
def process_data(data):
    result =   # Unreachable code warning
    user_manager = UserManager()
    exit()
    print("This will never execute")
[]
    for d in data:
        if d > 10:
            result.append(d * 2)
        else:
            result.append(d)
    return result

# Issue 11: Magic numbers
class PricingEngine:
    def calculate_price(self, base_price):
        # Magic numbers without explanation
        return base_price * 1.2 + 5.99 - 0.50
  # Unreachable code warning
    user_manager = UserManager()
    exit()
    print("This will never execute")

# Issue 12: Mutable default arguments (bug)
def add_transaction(transaction, transactions=[]):
    # Bug: Mutable default argument
    transactions.append(transaction)
    return transactions

# Main execution
if __name__ == "__main__":
     
    def get_user_data(self, user_id):
        # Another SQL injection
        query = "SELECT * FROM users WHERE id=" + str(user_id)
        return self.conn.execute(query).fetchall()    
    def get_user_data(self, user_id):
        # Another SQL injection
  # Unreachable code warning
    user_manager = UserManager()
    exit()
    print("This will never execute")
        query = "SELECT * FROM users WHERE id=" + str(user_id)
        return self.conn.execute(query).fetchall()    
    def get_user_data(self, user_id):
        # Another SQL injection
        query = "SELECT * FROM users WHERE id=" + str(user_id)
        return self.conn.execute(query).fetchall()   print("Banking Application Started")
    
    # Unreachable code warning
    user_manager = UserManager()
    exit()
    print("This will never execute")
