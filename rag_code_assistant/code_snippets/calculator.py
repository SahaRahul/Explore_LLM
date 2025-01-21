def add_numbers(a, b):
    return a + b

def subtract_numbers(a, b):
    return a - b

def multiply_numbers(a, b):
    return a * b

def divide_numbers(a, b):
    if b != 0:
        return a / b
    return "Division by zero error"

def calculate_addition(numbers):
    result = numbers[0]
    for number in numbers[1:]:
        result += number
    return result

def calculate_subtraction(numbers):
    result = numbers[0]
    for number in numbers[1:]:
        result -= number
    return result

def calculate_multiplication(numbers):
    result = numbers[0]
    for number in numbers[1:]:
        result *= number
    return result