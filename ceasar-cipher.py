# List of letters used to calculate the shift based on index positions
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

# Gather user preferences and input data
direction = input("Type 'encode' to encrypt, type 'decode' to decrypt:\n").lower()
text = input("Type your message:\n").lower()
shift = int(input("Type the shift number:\n"))

def encrypt(original_text, shift_amount):
    cipher_text = ""
    for letter in original_text:
        # Check if the character is in our alphabet (ignores spaces/numbers/symbols)
        if letter in alphabet:
            # Find the original index and add the shift
            shifted_position = alphabet.index(letter) + shift_amount
            # Use modulo to wrap back to the start if position > 25
            shifted_position %= len(alphabet)
            cipher_text += alphabet[shifted_position]
        else:
            # Keep non-alphabet characters (like spaces) as they are
            cipher_text += letter
    return cipher_text

def decrypt(original_text, shift_amount):
    cipher_text = ""
    for letter in original_text:
        if letter in alphabet:
            # Subtract the shift to go backwards through the alphabet
            shifted_position = alphabet.index(letter) - shift_amount
            # Modulo works for negative numbers in Python, wrapping to the end
            shifted_position %= len(alphabet)
            cipher_text += alphabet[shifted_position]
        else:
            cipher_text += letter
    return cipher_text

def ceasar(original_text, shift_amount):
    # Determine which function to call based on user's choice
    if direction == 'encode':
        cipher = encrypt(original_text=original_text, shift_amount=shift_amount)
        print(f"Here is the encrypted message: {cipher}")
    elif direction == 'decode':
        cipher = decrypt(original_text=original_text, shift_amount=shift_amount)
        print(f"Here is the decrypted message: {cipher}")
    else:
        # Basic error handling for invalid direction inputs
        print("Please enter either 'encode' or 'decode':")

# Call the main function to execute the logic
ceasar(original_text=text, shift_amount=shift)
