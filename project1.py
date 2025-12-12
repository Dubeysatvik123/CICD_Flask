import sqlite3
import os
import hashlib
import pickle
import random
import subprocess

# -----------------------------
# HARD CODED CREDENTIALS  ❌
# -----------------------------
DB_USER = "admin"
DB_PASSWORD = "123456"   # Hardcoded password

# -----------------------------
# SQL INJECTION VULNERABILITY ❌
# -----------------------------
def get_user_details(username):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    # SQL Injection: concatenated query
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)

    result = cursor.fetchall()
    conn.close()
    return result


# -----------------------------
# COMMAND INJECTION VULNERABILITY ❌
# -----------------------------
def ping_server(ip):
    # User-controlled input directly passed into shell
    return os.system(f"ping -c 1 {ip}")


# -----------------------------
# INSECURE RANDOM ❌
# -----------------------------
def generate_otp():
    # predictable OTP
    return random.randint(1000, 9999)


# -----------------------------
# INSECURE HASHING (MD5) ❌
# -----------------------------
def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()


# -----------------------------
# LOGIC BUG: wrong even check ❌
# -----------------------------
def is_even(num):
    return num % 2 == 1   # WRONG on purpose


# -----------------------------
# PATH TRAVERSAL ❌
# -----------------------------
def read_file(filename):
    # No validation
    with open(filename, "r") as f:
        return f.read()


# -----------------------------
# INSECURE DESERIALIZATION ❌
# -----------------------------
def load_user_profile(payload):
    # Direct pickle load from user input
    return pickle.loads(payload)


# -----------------------------
# DANGEROUS EVAL ❌
# -----------------------------
def evaluate_expression(expr):
    return eval(expr)


# -----------------------------
# BUG + UNUSED CODE ❌
# -----------------------------
def calculate_discount(price):
    unused_var = 999

    if price < 0:
        return "Invalid"  # No exception, logic bug
    
    # Bug: wrong formula (should be * 0.9)
    discount = price * 1.9  
    return discount


# -----------------------------
# DEAD CODE BLOCK ❌
# -----------------------------
def dead_code_example():
    return 1
    x = 5  # never executed
    return x


# -----------------------------
# AUTH FUNCTION with LOGIC BUG ❌
# -----------------------------
def authenticate(user, password):
    if user == DB_USER and password != DB_PASSWORD:
        return True  # WRONG logic
    return False
