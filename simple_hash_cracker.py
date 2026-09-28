#!/usr/bin/env python3
# simple_hash_cracker.py
# A simple password hash cracker for LEARNING purposes.
# Uses a wordlist to test common passwords against a hash.
# Much slower than hashcat, but works on any device.

import hashlib
import os
import sys
import time


def hash_password(password, algorithm="sha256"):
    """Hash a password using the chosen algorithm."""
    encoded = password.encode()
    if algorithm == "md5":
        return hashlib.md5(encoded).hexdigest()
    elif algorithm == "sha1":
        return hashlib.sha1(encoded).hexdigest()
    elif algorithm == "sha256":
        return hashlib.sha256(encoded).hexdigest()
    elif algorithm == "sha512":
        return hashlib.sha512(encoded).hexdigest()
    else:
        raise ValueError("Unsupported algorithm")


def crack_hash(target_hash, wordlist_file, algorithm="sha256"):
    """Try each word in the wordlist to crack the hash."""
    if not os.path.exists(wordlist_file):
        print(f"❌ Wordlist not found: {wordlist_file}")
        return None

    # Count total lines first (for progress)
    with open(wordlist_file, "r", errors="ignore") as f:
        total = sum(1 for _ in f)

    print(f"📋 Wordlist: {wordlist_file}")
    print(f"📊 Total words to try: {total}")
    print(f"🔐 Algorithm: {algorithm}")
    print(f"🎯 Target hash: {target_hash}")
    print()
    print("Starting...")
    print()

    start_time = time.time()
    tried = 0
    found = None

    with open(wordlist_file, "r", errors="ignore") as f:
        for line in f:
            word = line.strip()
            if not word:
                continue

            tried += 1
            hashed = hash_password(word, algorithm)

            if hashed == target_hash:
                found = word
                break

            # Progress every 1000 attempts
            if tried % 1000 == 0:
                elapsed = time.time() - start_time
                rate = tried / elapsed if elapsed > 0 else 0
                print(f"  Tried {tried} words ({rate:.0f} words/sec)")

    elapsed = time.time() - start_time

    print()
    print("=" * 50)
    if found:
        print(f"✅ CRACKED!")
        print(f"   Password: {found}")
        print(f"   Tried: {tried} words")
        print(f"   Time: {elapsed:.2f} seconds")
    else:
        print(f"❌ Not found in this wordlist.")
        print(f"   Tried: {tried} words")
        print(f"   Time: {elapsed:.2f} seconds")
    print("=" * 50)

    return found


def generate_test_hash():
    """Helper: generate a hash from a test password."""
    password = input("Enter a password to hash: ")
    algorithm = input("Algorithm (md5/sha1/sha256/sha512) [sha256]: ").strip() or "sha256"
    hashed = hash_password(password, algorithm)
    print()
    print(f"Password:  {password}")
    print(f"Algorithm: {algorithm}")
    print(f"Hash:      {hashed}")
    return hashed


def main():
    print("=" * 50)
    print("   SIMPLE HASH CRACKER (Learning Tool)")
    print("=" * 50)
    print()
    print("⚠️  For LEARNING only.")
    print("   Only use on hashes you own or have permission to test.")
    print()

    while True:
        print("1. Generate a test hash from a password")
        print("2. Crack a hash")
        print("3. Exit")
        choice = input("Choice: ").strip()

        if choice == "1":
            print()
            generate_test_hash()
            print()

        elif choice == "2":
            print()
            target = input("Enter the hash to crack: ").strip()
            algorithm = input("Algorithm (md5/sha1/sha256/sha512) [sha256]: ").strip() or "sha256"
            wordlist = input("Path to wordlist [wordlist.txt]: ").strip() or "wordlist.txt"
            print()
            crack_hash(target, wordlist, algorithm)
            print()

        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
