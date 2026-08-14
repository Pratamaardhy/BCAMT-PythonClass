# from modul import calculate_circle_area
# print(calculate_circle_area(5))  # Output: 78.53981633974483a

import requests

response = requests.get("https://github.com")
print(response.status_code)  # Output: 200
