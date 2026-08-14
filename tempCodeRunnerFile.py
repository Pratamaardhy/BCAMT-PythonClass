"""Challenge: Testing & Debugging

This file contains solutions for six Python challenges:
1. Searching Algorithm
2. Sorting Algorithm
3. Roman Number conversion
4. Fibonacci Number
5. Odd-even number classification
6. Most frequent word

All implementations are written without using external libraries.
"""


# ---------------------------
# Challenge 1: Searching
# ---------------------------

def linear_search(arr, target):
    """Return the index of target in arr using linear search.
    Returns -1 when the target is not found.
    """
    if not isinstance(arr, list):
        raise TypeError("arr must be a list")

    for index, value in enumerate(arr):
        if value == target:
            return index
    return -1


def binary_search(arr, target):
    """Return the index of target in a sorted list using binary search.
    Returns -1 when the target is not found.
    """
    if not isinstance(arr, list):
        raise TypeError("arr must be a list")

    left = 0
    right = len(arr) - 1

    while left <= right:
        mid = (left + right) // 2

        if arr[mid] == target:
            return mid
        if arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1


# ---------------------------
# Challenge 2: Sorting
# ---------------------------

def bubble_sort(arr):
    """Sort a list in ascending order using Bubble Sort."""
    if not isinstance(arr, list):
        raise TypeError("arr must be a list")

    result = arr[:]
    length = len(result)

    for i in range(length):
        swapped = False
        for j in range(0, length - i - 1):
            if result[j] > result[j + 1]:
                result[j], result[j + 1] = result[j + 1], result[j]
                swapped = True
        if not swapped:
            break

    return result


def selection_sort(arr):
    """Sort a list in ascending order using Selection Sort."""
    if not isinstance(arr, list):
        raise TypeError("arr must be a list")

    result = arr[:]
    length = len(result)

    for i in range(length):
        min_index = i
        for j in range(i + 1, length):
            if result[j] < result[min_index]:
                min_index = j
        if min_index != i:
            result[i], result[min_index] = result[min_index], result[i]

    return result


def insertion_sort(arr):
    """Sort a list in ascending order using Insertion Sort."""
    if not isinstance(arr, list):
        raise TypeError("arr must be a list")

    result = arr[:]
    length = len(result)

    for i in range(1, length):
        key = result[i]
        j = i - 1

        while j >= 0 and result[j] > key:
            result[j + 1] = result[j]
            j -= 1

        result[j + 1] = key

    return result


# ---------------------------
# Challenge 3: Roman Number
# ---------------------------

def roman_to_int(roman):
    """Convert a Roman numeral to an integer.
    Example: MMXXV -> 2025.
    """
    if not isinstance(roman, str):
        raise TypeError("roman must be a string")

    roman = roman.strip()
    if roman == "":
        raise ValueError("Roman numeral cannot be empty")

    roman_map = {
        'I': 1,
        'V': 5,
        'X': 10,
        'L': 50,
        'C': 100,
        'D': 500,
        'M': 1000,
    }

    valid_chars = set(roman_map.keys())
    for ch in roman:
        if ch.upper() not in valid_chars:
            raise ValueError(f"Invalid Roman numeral character: {ch}")

    total = 0
    previous_value = 0

    for ch in reversed(roman.upper()):
        value = roman_map[ch]
        if value < previous_value:
            total -= value
        else:
            total += value
        previous_value = value

    return total


# ---------------------------
# Challenge 4: Fibonacci
# ---------------------------

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


# ---------------------------
# Challenge 5: Odd and Even
# ---------------------------

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


# ---------------------------
# Challenge 6: Most Frequent Word
# ---------------------------

def most_frequent_word(text):
    """Return a dictionary with the most common word and its count.
    Example: most_frequent_word('Hallo aku dan ...') -> {'word': 'lucu', 'count': 2}
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")

    cleaned_text = text.strip()
    if cleaned_text == "":
        raise ValueError("text cannot be empty")

    words = []
    for token in cleaned_text.lower().replace('-', ' ').split():
        cleaned_word = ""
        for ch in token:
            if ch.isalpha() or ch.isdigit():
                cleaned_word += ch
        if cleaned_word:
            words.append(cleaned_word)

    if not words:
        raise ValueError("No valid words found in the text")

    frequency = {}
    for word in words:
        if word in frequency:
            frequency[word] += 1
        else:
            frequency[word] = 1

    most_word = ""
    most_count = 0
    for word, count in frequency.items():
        if count > most_count:
            most_word = word
            most_count = count

    return {
        'word': most_word,
        'count': most_count,
    }


# ---------------------------
# Testing and debugging
# ---------------------------

def run_tests():
    """Run positive and negative tests for every challenge."""

    # Challenge 1 tests
    assert linear_search([2, 5, 8, 12, 16, 23, 38, 56, 72, 91], 23) == 5
    assert linear_search([2, 5, 8, 12, 16, 23, 38, 56, 72, 91], 100) == -1
    assert binary_search([2, 5, 8, 12, 16, 23, 38, 56, 72, 91], 23) == 5
    assert binary_search([2, 5, 8, 12, 16, 23, 38, 56, 72, 91], 99) == -1

    # Challenge 2 tests
    assert bubble_sort([4, 7, 8, 2, 5, 10, 15, 20, 21, 16, 19]) == [2, 4, 5, 7, 8, 10, 15, 16, 19, 20, 21]
    assert selection_sort([4, 7, 8, 2, 5, 10, 15, 20, 21, 16, 19]) == [2, 4, 5, 7, 8, 10, 15, 16, 19, 20, 21]
    assert insertion_sort([4, 7, 8, 2, 5, 10, 15, 20, 21, 16, 19]) == [2, 4, 5, 7, 8, 10, 15, 16, 19, 20, 21]

    # Negative sorting test
    try:
        bubble_sort("not a list")
        raise AssertionError("bubble_sort should reject non-list input")
    except TypeError:
        pass

    # Challenge 3 tests
    assert roman_to_int("MMXXV") == 2025
    assert roman_to_int("IV") == 4
    assert roman_to_int("XLII") == 42

    try:
        roman_to_int("ABC")
        raise AssertionError("roman_to_int should reject invalid Roman numeral")
    except ValueError:
        pass

    # Challenge 4 tests
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

    # Challenge 5 tests
    result = find_even_odd_numbers(1, 10)
    assert result == {'even': [2, 4, 6, 8, 10], 'odd': [1, 3, 5, 7, 9]}

    try:
        find_even_odd_numbers(10, 1)
        raise AssertionError("find_even_odd_numbers should reject invalid range")
    except ValueError:
        pass

    # Challenge 6 tests
    sentence = "Hallo aku dan teman-temanku mempunyai kucing annabul lucu-lucu."
    assert most_frequent_word(sentence) == {'word': 'lucu', 'count': 2}

    try:
        most_frequent_word("")
        raise AssertionError("most_frequent_word should reject empty input")
    except ValueError:
        pass

    print("All tests passed successfully.")


if __name__ == "__main__":
    run_tests()
