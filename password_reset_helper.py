#!/usr/bin/env python3
# password_reset_helper.py
# A guide for technicians to reset passwords safely.

import os
import datetime


# Safety checklist
SAFETY_RULES = """
=== SAFETY CHECKLIST (READ FIRST) ===

Before resetting ANY password:
  [ ] Verify the user owns the device/account
  [ ] Get written permission (WhatsApp, SMS)
  [ ] Confirm the request is legitimate
  [ ] NEVER reset accounts you don't own
  [ ] NEVER log into a client's account "to help"

Breaking these = ILLEGAL in Kenya.
"""


def windows_steps():
    return """
=== WINDOWS PASSWORD RESET ===

Method A — Security Questions:
  1. At login screen, click "Reset password"
  2. Answer the security questions
  3. Set a new password

Method B — Another Admin Account:
  1. Log in as another admin
  2. Settings -> Accounts -> Other users
  3. Select user -> Change password

Method C — Password Reset Disk:
  1. Insert the disk at login
  2. Follow the wizard

Method D — Offline Reset (advanced):
  1. Boot from Windows install USB
  2. Access command prompt
  3. Replace utilman.exe with cmd.exe
  4. Reset password from cmd

Method E — Reinstall (last resort):
  - Data is LOST. Only if nothing else works.

Charge: KSh 1,000 - 2,500
"""


def android_steps():
    return """
=== ANDROID LOCK RESET ===

Method A — Google Account:
  1. Wrong PIN 5 times
  2. Click "Forgot pattern"
  3. Sign in with linked Google account
  4. Set a new lock

Method B — Find My Device:
  1. Go to google.com/android/find
  2. Sign in with the Google account
  3. Choose "Lock" -> set a new password remotely

Method C — Factory Reset (last resort):
  1. Recovery Mode -> Wipe data/factory reset
  2. ALL DATA WILL BE LOST
  3. Needs Google account to set up (FRP)

Charge: KSh 500 - 1,500
"""


def linux_steps():
    return """
=== LINUX PASSWORD RESET ===

Using Recovery Mode:
  1. Restart the computer
  2. At GRUB menu, choose "Advanced options"
  3. Choose "Recovery mode"
  4. Choose "root - Drop to root shell"
  5. Type: passwd username
  6. Enter new password twice
  7. Reboot

No old password needed.
Charge: KSh 1,000 - 2,500
"""


def online_steps():
    return """
=== ONLINE ACCOUNT RESET ===

IMPORTANT: You DO NOT reset online accounts for clients.
You GUIDE them. They do the work.

What to do:
  1. Open the "Forgot password" page
  2. Show them the options
  3. Help them access their email/phone
  4. Let THEM click the reset link

What NOT to do:
  - Never log in to their account
  - Never change their password for them
  - Never access their email

Charge: KSh 500 - 1,500 (guidance only)
"""


def log_job(system, client_name):
    """Log the reset in a file."""
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("password_resets_log.txt", "a") as f:
        f.write("=" * 50 + "\n")
        f.write(f"Date: {now}\n")
        f.write(f"System: {system}\n")
        f.write(f"Client: {client_name}\n")
        f.write(f"Technician: Felix Otieno\n")
        f.write("=" * 50 + "\n\n")


def main():
    print("=" * 50)
    print("   PASSWORD RESET HELPER")
    print("=" * 50)
    print()
    print(SAFETY_RULES)
    print()

    # Verify ownership
    owned = input("Does the client OWN this device/account? (y/n): ").lower()
    if owned != "y":
        print("STOP. Do not proceed. This could be illegal.")
        return

    permission = input("Do you have WRITTEN permission? (y/n): ").lower()
    if permission != "y":
        print("STOP. Get written permission first.")
        return

    print()
    print("What are you resetting?")
    print("1. Windows password")
    print("2. Android lock")
    print("3. Linux password")
    print("4. Online account (guidance only)")
    print()
    choice = input("Choice (1-4): ")

    client = input("Client name (for your log): ")

    print()
    if choice == "1":
        print(windows_steps())
        log_job("Windows", client)
    elif choice == "2":
        print(android_steps())
        log_job("Android", client)
    elif choice == "3":
        print(linux_steps())
        log_job("Linux", client)
    elif choice == "4":
        print(online_steps())
        log_job("Online (guidance)", client)
    else:
        print("Invalid choice.")
        return

    print()
    print("Logged to password_resets_log.txt")


if __name__ == "__main__":
    main()
