def add(a, b):
    return a - b  # BUG 1: Wrong logic (should be a + b)

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    return a / b

def factorial(n):
    if n == 0:
        return 1
    result = 1
    for i in range(1, n):  # BUG 2: Off-by-one (should be range(1, n+1))
        result *= i
    return result

def is_palindrome(s):
    return s == s[::-1]

def get_stats(numbers):
    total = sum(numbers)
    count = len(numbers)
    average = total / count
    return {
        "sum": total,
        "count": count,
        "average": average,
        "max": max(numbers),
        "min": min(numbers)
        # BUG 3: Missing "median" key that tests expect
    }
