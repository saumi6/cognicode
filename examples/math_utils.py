"""
Example math utility functions for testing the pytest generator
This file contains various mathematical functions to demonstrate test generation
"""

import math
from typing import List, Union

def calculate_area(length: float, width: float) -> float:
    """
    Calculate the area of a rectangle.
    
    Args:
        length: The length of the rectangle
        width: The width of the rectangle
        
    Returns:
        The area of the rectangle
        
    Raises:
        ValueError: If length or width is negative
    """
    if length < 0 or width < 0:
        raise ValueError("Length and width must be positive")
    return length * width

def fibonacci(n: int) -> int:
    """
    Calculate the nth Fibonacci number using recursion.
    
    Args:
        n: The position in the Fibonacci sequence (0-indexed)
        
    Returns:
        The nth Fibonacci number
        
    Raises:
        ValueError: If n is negative
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

def is_prime(n: int) -> bool:
    """
    Check if a number is prime.
    
    Args:
        n: The number to check
        
    Returns:
        True if the number is prime, False otherwise
    """
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True

def factorial(n: int) -> int:
    """
    Calculate the factorial of a number.
    
    Args:
        n: The number to calculate factorial for
        
    Returns:
        The factorial of n
        
    Raises:
        ValueError: If n is negative
    """
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)

def gcd(a: int, b: int) -> int:
    """
    Find the greatest common divisor of two numbers using Euclidean algorithm.
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        The greatest common divisor of a and b
    """
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a

def lcm(a: int, b: int) -> int:
    """
    Find the least common multiple of two numbers.
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        The least common multiple of a and b
        
    Raises:
        ValueError: If either number is zero
    """
    if a == 0 or b == 0:
        raise ValueError("LCM is not defined when one of the numbers is zero")
    return abs(a * b) // gcd(a, b)

def quadratic_roots(a: float, b: float, c: float) -> List[Union[float, complex]]:
    """
    Find the roots of a quadratic equation ax² + bx + c = 0.
    
    Args:
        a: Coefficient of x²
        b: Coefficient of x
        c: Constant term
        
    Returns:
        List of roots (may be real or complex)
        
    Raises:
        ValueError: If a is zero (not a quadratic equation)
    """
    if a == 0:
        raise ValueError("'a' cannot be zero for a quadratic equation")
    
    discriminant = b**2 - 4*a*c
    
    if discriminant >= 0:
        sqrt_discriminant = math.sqrt(discriminant)
        root1 = (-b + sqrt_discriminant) / (2*a)
        root2 = (-b - sqrt_discriminant) / (2*a)
        return [root1, root2]
    else:
        real_part = -b / (2*a)
        imaginary_part = math.sqrt(-discriminant) / (2*a)
        root1 = complex(real_part, imaginary_part)
        root2 = complex(real_part, -imaginary_part)
        return [root1, root2]

def power(base: float, exponent: int) -> float:
    """
    Calculate base raised to the power of exponent using iterative method.
    
    Args:
        base: The base number
        exponent: The exponent (must be integer)
        
    Returns:
        The result of base^exponent
    """
    if exponent == 0:
        return 1.0
    
    result = 1.0
    positive_exp = abs(exponent)
    
    for _ in range(positive_exp):
        result *= base
    
    return result if exponent > 0 else 1.0 / result

def average(numbers: List[Union[int, float]]) -> float:
    """
    Calculate the average of a list of numbers.
    
    Args:
        numbers: List of numbers
        
    Returns:
        The average of the numbers
        
    Raises:
        ValueError: If the list is empty or contains non-numeric values
    """
    if not numbers:
        raise ValueError("Cannot calculate average of empty list")
    
    total = 0
    for num in numbers:
        if not isinstance(num, (int, float)):
            raise ValueError("All elements must be numeric")
        total += num
    
    return total / len(numbers)

def median(numbers: List[Union[int, float]]) -> float:
    """
    Calculate the median of a list of numbers.
    
    Args:
        numbers: List of numbers
        
    Returns:
        The median of the numbers
        
    Raises:
        ValueError: If the list is empty
    """
    if not numbers:
        raise ValueError("Cannot calculate median of empty list")
    
    sorted_numbers = sorted(numbers)
    n = len(sorted_numbers)
    
    if n % 2 == 0:
        return (sorted_numbers[n//2 - 1] + sorted_numbers[n//2]) / 2
    else:
        return float(sorted_numbers[n//2])