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

def run_tests():
    assert roman_to_int("MMXXV") == 2025
    assert roman_to_int("IV") == 4
    assert roman_to_int("XLII") == 42

    try:
        roman_to_int("ABC")
        raise AssertionError("roman_to_int should reject invalid Roman numeral")
    except ValueError:
        pass
if __name__ == "__main__":
    run_tests()
    print("Challenge 3 tests passed successfully.")