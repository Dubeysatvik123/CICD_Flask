"""
Test cases for vulnerable_app.py
This will help achieve code coverage for SonarQube analysis
"""

import unittest
import sqlite3
import os
from vulnerable_app import (
    UserManager, DataProcessor, SecurityManager, 
    FileManager, BankAccount, TransactionManager,
    calculate_total, complex_business_logic, 
    process_data, PricingEngine, add_transaction
)

class TestUserManager(unittest.TestCase):
    def setUp(self):
        # Setup test database
        self.conn = sqlite3.connect(':memory:')
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE users 
                         (id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')
        cursor.execute("INSERT INTO users VALUES (1, 'admin', 'pass123')")
        self.conn.commit()
        
        self.user_manager = UserManager()
        self.user_manager.conn = self.conn
    
    def test_authenticate_user_success(self):
        """Test user authentication with valid credentials"""
        result = self.user_manager.authenticate_user('admin', 'pass123')
        self.assertIsNotNone(result)
    
    def test_authenticate_user_failure(self):
        """Test authentication with invalid credentials"""
        result = self.user_manager.authenticate_user('invalid', 'wrong')
        self.assertIsNone(result)
    
    def test_get_user_data(self):
        """Test retrieving user data by ID"""
        result = self.user_manager.get_user_data(1)
        self.assertTrue(len(result) > 0)

class TestDataProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = DataProcessor()
    
    def test_save_and_load_session(self):
        """Test session serialization"""
        data = {'user_id': 1, 'username': 'test'}
        serialized = self.processor.save_session(data)
        deserialized = self.processor.load_user_session(serialized)
        self.assertEqual(data, deserialized)

class TestSecurityManager(unittest.TestCase):
    def setUp(self):
        self.security = SecurityManager()
    
    def test_hash_password(self):
        """Test password hashing"""
        hashed = self.security.hash_password('password123')
        self.assertIsNotNone(hashed)
        self.assertEqual(len(hashed), 32)  # MD5 hash length
    
    def test_generate_token(self):
        """Test token generation"""
        token = self.security.generate_token()
        self.assertTrue(1000 <= token <= 9999)

class TestFileManager(unittest.TestCase):
    def setUp(self):
        self.file_manager = FileManager()
        # Create a test file
        with open('test_file.txt', 'w') as f:
            f.write('test content')
    
    def tearDown(self):
        # Cleanup
        if os.path.exists('test_file.txt'):
            os.remove('test_file.txt')
        if os.path.exists('app.log'):
            os.remove('app.log')
    
    def test_read_file(self):
        """Test file reading"""
        content = self.file_manager.read_file('test_file.txt')
        self.assertEqual(content, 'test content')
    
    def test_write_log(self):
        """Test log writing"""
        self.file_manager.write_log('Test log entry')
        self.assertTrue(os.path.exists('app.log'))

class TestBankAccount(unittest.TestCase):
    def test_withdraw(self):
        """Test withdrawal functionality"""
        account = BankAccount(1000)
        new_balance = account.withdraw(200)
        self.assertEqual(new_balance, 800)
    
    def test_withdraw_negative(self):
        """Test withdrawal with negative amount (bug test)"""
        account = BankAccount(1000)
        new_balance = account.withdraw(-200)
        self.assertEqual(new_balance, 1200)  # Bug allows this
    
    def test_deposit(self):
        """Test deposit functionality"""
        account = BankAccount(1000)
        try:
            account.deposit(500)
        except ZeroDivisionError:
            pass  # Expected due to bug
    
    def test_calculate_interest_positive(self):
        """Test interest calculation with positive rate"""
        account = BankAccount(1000)
        account.calculate_interest(0.05)
        self.assertEqual(account.balance, 1050)
    
    def test_calculate_interest_zero(self):
        """Test interest calculation with zero rate"""
        account = BankAccount(1000)
        account.calculate_interest(0)
        self.assertEqual(account.balance, 1000)

class TestTransactionManager(unittest.TestCase):
    def setUp(self):
        self.manager = TransactionManager()
    
    def test_process_payment_valid(self):
        """Test valid payment processing"""
        result = self.manager.process_payment(100)
        self.assertTrue(result)
    
    def test_process_payment_invalid(self):
        """Test invalid payment processing"""
        result = self.manager.process_payment(-100)
        self.assertIsNone(result)  # Due to exception swallowing

class TestUtilityFunctions(unittest.TestCase):
    def test_calculate_total(self):
        """Test total calculation"""
        items = [
            {'name': 'item1', 'price': 10},
            {'name': 'item2', 'price': 20}
        ]
        total = calculate_total(items)
        self.assertEqual(total, 30)
    
    def test_complex_business_logic_all_valid(self):
        """Test complex logic with valid inputs"""
        class MockUser:
            is_active = True
        
        class MockAccount:
            balance = 1000
        
        class MockTransaction:
            amount = 500
            type = "transfer"
        
        class MockSettings:
            allow_transfers = True
        
        result = complex_business_logic(
            MockUser(), MockAccount(), 
            MockTransaction(), MockSettings()
        )
        self.assertTrue(result)
    
    def test_complex_business_logic_none_user(self):
        """Test complex logic with None user"""
        result = complex_business_logic(None, None, None, None)
        self.assertFalse(result)
    
    def test_process_data(self):
        """Test data processing function"""
        result = process_data([5, 15, 8, 20])
        self.assertEqual(result, [5, 30, 8, 40])

class TestPricingEngine(unittest.TestCase):
    def test_calculate_price(self):
        """Test price calculation"""
        engine = PricingEngine()
        price = engine.calculate_price(100)
        self.assertEqual(price, 125.49)

class TestMutableDefaults(unittest.TestCase):
    def test_add_transaction_bug(self):
        """Test mutable default argument bug"""
        result1 = add_transaction('tx1')
        result2 = add_transaction('tx2')
        # Bug: result2 contains both transactions
        self.assertEqual(len(result2), 2)

if __name__ == '__main__':
    # Run tests with coverage
    unittest.main(verbosity=2)
