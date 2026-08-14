import matplotlib.pyplot as plt
import numpy as np

categories = ['aple', 'bluebery', 'cherry', 'orange']
values = [23, 45, 56, 78]


plt.bar(categories, values, color=['red', 'blue', 'brown', 'orange'])  # Custom colors for each bar

plt.xlabel('Kategori')
plt.ylabel('Jumlah')
plt.title('Jumlah Buah Berdasarkan Kategori')

plt.show()
