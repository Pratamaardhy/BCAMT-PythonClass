"""Challenge 2 - Sorting Algorithm

Array: [4, 7, 8, 2, 5, 10, 15, 20, 21, 16, 19]

Implementasi:
- Bubble Sort
- Selection Sort
- Insertion Sort
- Testing dan debugging
"""


def bubble_sort(arr):
    """Urutkan list ascending menggunakan Bubble Sort."""
    if not isinstance(arr, list):
        raise TypeError("arr harus berupa list")

    result = arr[:]
    n = len(result)

    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if result[j] > result[j + 1]:
                result[j], result[j + 1] = result[j + 1], result[j]
                swapped = True
        if not swapped:
            break

    return result


def selection_sort(arr):
    """Urutkan list ascending menggunakan Selection Sort."""
    if not isinstance(arr, list):
        raise TypeError("arr harus berupa list")

    result = arr[:]
    n = len(result)

    for i in range(n):
        min_index = i
        for j in range(i + 1, n):
            if result[j] < result[min_index]:
                min_index = j
        if min_index != i:
            result[i], result[min_index] = result[min_index], result[i]

    return result


def insertion_sort(arr):
    """Urutkan list ascending menggunakan Insertion Sort."""
    if not isinstance(arr, list):
        raise TypeError("arr harus berupa list")

    result = arr[:]
    n = len(result)

    for i in range(1, n):
        key = result[i]
        j = i - 1

        while j >= 0 and result[j] > key:
            result[j + 1] = result[j]
            j -= 1

        result[j + 1] = key

    return result


def run_tests():
    arr = [4, 7, 8, 2, 5, 10, 15, 20, 21, 16, 19]
    expected = [2, 4, 5, 7, 8, 10, 15, 16, 19, 20, 21]

    # Positive cases
    assert bubble_sort(arr) == expected
    assert selection_sort(arr) == expected
    assert insertion_sort(arr) == expected

    # Negative cases
    try:
        bubble_sort("bukan list")
        raise AssertionError("bubble_sort harus menolak input bukan list")
    except TypeError:
        pass

    try:
        selection_sort("bukan list")
        raise AssertionError("selection_sort harus menolak input bukan list")
    except TypeError:
        pass

    try:
        insertion_sort("bukan list")
        raise AssertionError("insertion_sort harus menolak input bukan list")
    except TypeError:
        pass

    print("Challenge 2 tests passed successfully.")


if __name__ == "__main__":
    arr = [4, 7, 8, 2, 5, 10, 15, 20, 21, 16, 19]
    print("Array awal:", arr)
    print("Bubble Sort:", bubble_sort(arr))
    print("Selection Sort:", selection_sort(arr))
    print("Insertion Sort:", insertion_sort(arr))
    run_tests()
