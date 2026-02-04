import random

# --- DATA STRUCTURES ---
# Lists containing all possible characters for the password
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

print("Welcome to the CipherSmith (PyPassword Generator)!")

# --- USER INPUT ---
# We cast the inputs to integers (int) so we can use them in math operations
nr_letters = int(input("How many letters would you like in your password?\n"))
nr_symbols = int(input(f"How many symbols would you like?\n"))
nr_numbers = int(input(f"How many numbers would you like?\n"))

# Calculate the total length of the password to determine loop range
nr_total = nr_letters + nr_symbols + nr_numbers

password = ""

# --- PASSWORD GENERATION LOOP ---
# We loop through the total number of characters needed.
# Note: This logic builds the password in a specific order (Letter -> Symbol -> Number)
for num in range(0, nr_total + 1):
    
    # Check if user still needs letters, add one, and decrease the count
    if nr_letters > 0:
        password += random.choice(letters)
        nr_letters -= 1
        
    # Check if user still needs symbols
    if nr_symbols > 0:
        password += random.choice(symbols)
        nr_symbols -= 1
        
    # Check if user still needs numbers
    if nr_numbers > 0:
        password += random.choice(numbers)
        nr_numbers -= 1

# --- FINAL OUTPUT ---
print(f"Your password is: {password}")
