from calculator import add, subtract, multiply, divide, factorial, is_palindrome, get_stats

def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0

def test_subtract():
    assert subtract(5, 3) == 2
    assert subtract(0, 5) == -5

def test_multiply():
    assert multiply(3, 4) == 12
    assert multiply(-2, 5) == -10

def test_divide():
    assert divide(10, 2) == 5.0
    assert divide(7, 2) == 3.5

def test_factorial():
    assert factorial(0) == 1
    assert factorial(1) == 1
    assert factorial(5) == 120
    assert factorial(6) == 720

def test_is_palindrome():
    assert is_palindrome("racecar") == True
    assert is_palindrome("hello") == False

def test_get_stats():
    stats = get_stats([1, 2, 3, 4, 5])
    assert stats["sum"] == 15
    assert stats["count"] == 5
    assert stats["average"] == 3.0
    assert stats["max"] == 5
    assert stats["min"] == 1
    assert stats["median"] == 3  # BUG 3 will catch this
