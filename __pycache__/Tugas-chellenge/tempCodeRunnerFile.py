def linear_search(arr, target):
    for index, value in enumerate(arr):
        if value == target:
            return index
    return -1


array = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
target = 23

result = linear_search(array, target)
print(f"Angka {target} ditemukan pada index: {result}")