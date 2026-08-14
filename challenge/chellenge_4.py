def fibonacci_number(n):
    """Return the nth Fibonacci number.
    Example: fibonacci_number(20) -> 6765
    """
    if not isinstance(n, int):
        raise TypeError("n must be an integer")
    if n < 0:
        raise ValueError("n must be greater than or equal to 0")

    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

def run_tests():
    assert fibonacci_number(0) == 0
    assert fibonacci_number(1) == 1
    assert fibonacci_number(10) == 55
    assert fibonacci_number(20) == 6765

    try:
        fibonacci_number(-3)
        raise AssertionError("fibonacci_number should reject negative values")
    except ValueError:
        pass

    try:
        fibonacci_number("20")
        raise AssertionError("fibonacci_number should reject non-integer value")
    except TypeError:
        pass

if __name__ == "__main__":
    run_tests()
    print("Challenge 4 tests passed successfully.")