#!/usr/bin/env python3
# advanced_password.py
# Advanced password generator with options.

import random
import string


def generate_password(length=16, use_upper=True, use_lower=True,
                       use_digits=True, use_symbols=True):
    """Generate a password with the chosen options."""
    # Build the pool of characters
    pool = ""
    if use_upper:
        pool += string.ascii_uppercase
    if use_lower:
        pool += string.ascii_lowercase
    if use_digits:
        pool += string.digits
    if use_symbols:
        pool += string.punctuation

    # Make sure we have at least one option
    if pool == "":
        return "ERROR: No characters selected"

    # Ensure the password has at least one of each chosen type
    password = []
    if use_upper:
        password.append(random.choice(string.ascii_uppercase))
    if use_lower:
        password.append(random.choice(string.ascii_lowercase))
    if use_digits:
        password.append(random.choice(string.digits))
    if use_symbols:
        password.append(random.choice(string.punctuation))

    # Fill the rest with random characters
    while len(password) < length:
        password.append(random.choice(pool))

    # Shuffle so the required characters aren't at the start
    random.shuffle(password)

    return "".join(password)


def check_strength(password):
    """Score the password strength."""
    score = 0
    if len(password) >= 8: score += 1
    if len(password) >= 12: score += 1
    if len(password) >= 16: score += 1
    if any(c.isupper() for c in password): score += 1
    if any(c.islower() for c in password): score += 1
    if any(c.isdigit() for c in password): score += 1
    if any(c in string.punctuation for c in password): score += 1

    if score <= 3:
        return "WEAK"
    elif score <= 5:
        return "MEDIUM"
    else:
        return "STRONG"


def main():
    print("=" * 50)
    print("   ADVANCED PASSWORD GENERATOR")
    print("=" * 50)
    print()

    # Ask for settings
    try:
        length = int(input("Password length (8-64): "))
        if length < 8 or length > 64:
            print("Length must be between 8 and 64.")
            return
    except:
        print("Invalid number.")
        return

    use_upper = input("Include UPPERCASE? (y/n): ").lower() == "y"
    use_lower = input("Include lowercase? (y/n): ").lower() == "y"
    use_digits = input("Include digits? (y/n): ").lower() == "y"
    use_symbols = input("Include symbols? (y/n): ").lower() == "y"

    print()
    print("Generating 5 options for you...")
    print()

    for i in range(1, 6):
        pwd = generate_password(length, use_upper, use_lower, use_digits, use_symbols)
        strength = check_strength(pwd)
        print(f"Option {i}: {pwd}")
        print(f"          Length: {len(pwd)} | Strength: {strength}")
        print()

    # Save to file
    save = input("Save these to a file? (y/n): ").lower()
    if save == "y":
        with open("passwords.txt", "a") as f:
            f.write("=" * 50 + "\n")
            f.write(f"Generated: {__import__('datetime').datetime.now()}\n")
            f.write(f"Length: {length}\n")
            f.write(f"Saved by: Felix\n\n")
            for i in range(1, 6):
                pwd = generate_password(length, use_upper, use_lower, use_digits, use_symbols)
                f.write(f"{pwd}\n")
            f.write("\n")
        print("Saved to passwords.txt")

    print("Done.")


if __name__ == "__main__":
    main()
