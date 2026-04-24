from collections import Counter
# Create your tests here.
shoes = input(int("Enter no of shoes "))
size = [2,3,4,5,6,8,7,6,5,18]
a = Counter(size)
print(a.items())
customers = input(int("Enter no of customers "))