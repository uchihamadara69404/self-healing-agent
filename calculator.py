def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b

def factorial(n):
    if n == 0:
        return 1
    result = 1
    for i in range(1, n+1):
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
        "min": min(numbers),
        "median": sum(numbers) / len(numbers)
    }