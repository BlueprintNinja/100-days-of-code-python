import art

# Display the application branding
print(art.logo)
print("Welcome to Zenith Computer!")

# Dictionary to map string symbols to their corresponding mathematical functions
computer_functions = {}
operators = ["+", "-", "*", "/"]
operator = ""
continued = True
continue_with_result = ""


# Define core mathematical operations
def add(n1, n2):
    return n1 + n2


def subtract(n1, n2):
    return n1 - n2


def multiply(n1, n2):
    return n1 * n2


def divide(n1, n2):
    return n1 / n2


# Populate the dispatch dictionary with the function references
computer_functions["+"] = add
computer_functions["-"] = subtract
computer_functions["*"] = multiply
computer_functions["/"] = divide

# Get the initial starting value
first = float(input("What is your first number? "))

# Main application loop
while continued:

    # Input validation: Ensure the user provides a valid mathematical operator
    while operator not in operators:
        operator = input("What operator? (+, -, *, /)")
        if operator not in operators:
            print("Please enter a valid operator")

    second = float(input("What is your second number? "))

    # Execute the calculation by fetching the function from the dictionary
    # and immediately calling it with 'first' and 'second'
    first = computer_functions[operator](first, second)

    # Reset operator for the next potential iteration
    operator = ""

    print("The result is", first)

    # Ask the user if they want to perform another calculation on the current result
    while continue_with_result not in ["y", "n"]:
        continue_with_result = input(f"Would you like to continue working with the result {first}? (y/n)")

        if continue_with_result == "y":
            continued = True
        elif continue_with_result == "n":
            continued = False

    # Reset the choice variable to allow the validation loop to run again next time
    continue_with_result = ""
