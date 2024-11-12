import random

# Set the seed
random.seed(42)

# Your list
my_list = [1, 2, 3, 4, 5]

# Shuffle the list
for i in range(0, 9):
    random.shuffle(my_list)
    print(my_list)

print(my_list)
