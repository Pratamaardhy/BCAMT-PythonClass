"""Challenge 1 - Searching Algorithm

Array: [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
Target: 23

Implementasi:
- Linear Search
- Binary Search
- Testing dan debugging
"""


def linear_search(arr, target):
    """Mencari posisi target dengan Linear Search."""
    if not isinstance(arr, list):
        raise TypeError("arr harus berupa list")

    for index, value in enumerate(arr):
        if value == target:
            return index
    return -1


def binary_search(arr, target):
    """Mencari posisi target dengan Binary Search pada list terurut."""
    if not isinstance(arr, list):
        raise TypeError("arr harus berupa list")

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


def run_tests():
    arr = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]

    # Positive cases
    assert linear_search(arr, 23) == 5
    assert binary_search(arr, 23) == 5

    # Negative cases
    assert linear_search(arr, 99) == -1
    assert binary_search(arr, 99) == -1

    # Validation error cases
    try:
        linear_search("bukan list", 23)
        raise AssertionError("linear_search harus menolak input bukan list")
    except TypeError:
        pass

    try:
        binary_search("bukan list", 23)
        raise AssertionError("binary_search harus menolak input bukan list")
    except TypeError:
        pass

    print("Challenge 1 tests passed successfully.")


if __name__ == "__main__":
    print("Array:", [2, 5, 8, 12, 16, 23, 38, 56, 72, 91])
    print("Posisi angka 23 dengan Linear Search:", linear_search([2, 5, 8, 12, 16, 23, 38, 56, 72, 91], 23))
    print("Posisi angka 23 dengan Binary Search:", binary_search([2, 5, 8, 12, 16, 23, 38, 56, 72, 91], 23))
    run_tests()
