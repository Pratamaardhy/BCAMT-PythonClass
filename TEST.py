
def number_check(number):
    if number%2 == 0:
        print(f"{number} angka genap")
    else:
        print(f"{number} angka ganjil")
    return number_check

for i in range(1, 100):
    number_check(i)


        



# def multiplication(a, b):
#     return a * b

# result = multiplication(5, 10)
# print(result)

# def showMessage(message):
#     print(message)
#     showMessage("Hello World")

# for i in range(1,100):
#     if i % 3 == 0 and i % 5 == 0:
#         print("FizzBuzz")
#     elif i % 3 == 0:
#         print("Fizz")
#     elif i % 5 == 0:
#         print("Buzz")
#     else:
#         print(i)


# for i in range (5):
#     print("Hello World" + str(i))

# juara_dunia = 5

# # Conditional statement berdasarkan instruksi
# if juara_dunia > 5:
#     print("World Champion #5")
# elif juara_dunia < 5:
#     print("World Champion #0")
# else:
#     print("Bukan World Champions") 
    
    #  name: "Ardi"
    #  age: 25
    #  nasionality: ["Indonesian", "American", "British"]
    #  if person['age'] > 18:
    #      print(f"Hello, my name is {name}")


# print(f"Hello, my name is {person['name']}, I am {person['age']} years old, and I am {person['nasionality'][0]}.")

# number = 10
# number2 = 5
# print(f"Hello, the average of {number} and {number2} is {(number + number2) / 2}.")