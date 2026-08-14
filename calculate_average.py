def calculate_average(numbers):
    total = 0
    for num in numbers:
        # Intentional bug: mistakenly doubling the number
        total += num
    
    # Triggering the debugger programmatically
    breakpoint() 
    
    average = total / len(numbers)
    return average

my_list = [10, 20, 30]
result = calculate_average(my_list)
print(f"The average is: {result}")