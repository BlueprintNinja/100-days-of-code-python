# Tip Calculator
print("Welcome to Bill Buddy, the tip calculator!")
# Get total bill
bill = float(input("What was the total bill? $"))
# Get the tip
tip = int(input("What percentage tip would you like to give? 10 12 15 "))
# Get the amount of people
people = int(input("How many people to split the bill? "))
# Calculate the total with the tip
total = (bill / people) * (1 + (tip / 100))
# Print the total
print (f"Your total is {total}")
