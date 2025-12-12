import pytest
from unittest.mock import patch, MagicMock
import pickle
import vulnerable_app


# -----------------------------
# TEST: SQL Injection function
# -----------------------------
@patch("sqlite3.connect")
def test_get_user_details(mock_connect):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchall.return_value = [("admin", "test")]

    result = vulnerable_app.get_user_details("admin")
    assert result == [("admin", "test")]


# -----------------------------
# TEST: Command Injection (mocked)
# -----------------------------
@patch("os.system")
def test_ping_server(mock_system):
    mock_system.return_value = 0
    output = vulnerable_app.ping_server("127.0.0.1")
    assert output == 0
    mock_system.assert_called_once()


# -----------------------------
# TEST: Insecure random OTP
# -----------------------------
def test_generate_otp():
    otp = vulnerable_app.generate_otp()
    assert 1000 <= otp <= 9999  # At least check range


# -----------------------------
# TEST: Weak hashing (MD5)
# -----------------------------
def test_hash_password():
    hashed = vulnerable_app.hash_password("password")
    assert len(hashed) == 32  # MD5 length


# -----------------------------
# TEST: Logic bug (is_even)
# -----------------------------
def test_is_even():
    assert vulnerable_app.is_even(2) is False  # wrong logic
    assert vulnerable_app.is_even(3) is True   # wrong logic on purpose


# -----------------------------
# TEST: Path traversal (mocked file)
# -----------------------------
@patch("builtins.open", new_callable=MagicMock)
def test_read_file(mock_open):
    mock_file = MagicMock()
    mock_file.read.return_value = "Hello"
    mock_open.return_value.__enter__.return_value = mock_file

    data = vulnerable_app.read_file("test.txt")
    assert data == "Hello"


# -----------------------------
# TEST: Insecure deserialization
# -----------------------------
def test_load_user_profile():
    payload = pickle.dumps({"name": "john"})
    profile = vulnerable_app.load_user_profile(payload)
    assert profile["name"] == "john"


# -----------------------------
# TEST: Dangerous eval
# -----------------------------
def test_evaluate_expression():
    assert vulnerable_app.evaluate_expression("1 + 2") == 3


# -----------------------------
# TEST: Logic bug in discount
# -----------------------------
def test_calculate_discount():
    assert vulnerable_app.calculate_discount(100) == 190  # incorrect logic
    assert vulnerable_app.calculate_discount(-1) == "Invalid"


# -----------------------------
# DEAD CODE TEST (just call)
# -----------------------------
def test_dead_code():
    assert vulnerable_app.dead_code_example() == 1


# -----------------------------
# AUTH function logic bug
# -----------------------------
def test_authenticate():
    # Wrong logic: password incorrect but returns True
    assert vulnerable_app.authenticate("admin", "wrongpass") is True
    assert vulnerable_app.authenticate("admin", "123456") is False
