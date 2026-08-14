def find_even_odd_numbers(start, end):
    """Return two lists: even numbers and odd numbers from start to end.
    Example: find_even_odd_numbers(1, 10) -> ({'even': [2, 4, 6, 8, 10], 'odd': [1, 3, 5, 7, 9]})
    """
    if not isinstance(start, int) or not isinstance(end, int):
        raise TypeError("start and end must be integers")
    if start > end:
        raise ValueError("start must be less than or equal to end")

    even_numbers = []
    odd_numbers = []

    for number in range(start, end + 1):
        if number % 2 == 0:
            even_numbers.append(number)
        else:
            odd_numbers.append(number)

    return {
        'even': even_numbers,
        'odd': odd_numbers,
    }

def run_tests():
    result = find_even_odd_numbers(1, 10)
    assert result == {'even': [2, 4, 6, 8, 10], 'odd': [1, 3, 5, 7, 9]}

    result = find_even_odd_numbers(-5, 5)
    assert result == {'even': [-4, -2, 0, 2, 4], 'odd': [-5, -3, -1, 1, 3, 5]}

    try:
        find_even_odd_numbers(10, 1)
        raise AssertionError("find_even_odd_numbers should reject start > end")
    except ValueError:
        pass

    try:
        find_even_odd_numbers("1", "10")
        raise AssertionError("find_even_odd_numbers should reject non-integer values")
    except TypeError:
        pass

if __name__ == "__main__":
    run_tests()
    print("Challenge 5 tests passed successfully.")