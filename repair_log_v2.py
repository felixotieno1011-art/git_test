#!/usr/bin/env python3
# repair_log_v2.py
# Repair tracking tool with JSON storage.
# Features: add, view, stats, search, receipt.

import json
import os
import datetime


LOG_FILE = "repairs.json"


def load_repairs():
    """Load all repairs from the JSON file."""
    if not os.path.exists(LOG_FILE):
        return []
    try:
        with open(LOG_FILE, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️  Could not read {LOG_FILE}: {e}")
        return []


def save_repairs(repairs):
    """Save repairs safely using a temp file."""
    temp_file = LOG_FILE + ".tmp"
    try:
        with open(temp_file, "w") as f:
            json.dump(repairs, f, indent=2)
        os.replace(temp_file, LOG_FILE)
    except Exception as e:
        print(f"❌ Error saving: {e}")
        if os.path.exists(temp_file):
            os.remove(temp_file)


def add_repair():
    """Add a new repair."""
    print()
    print("=== Add New Repair ===")

    repairs = load_repairs()

    # Next number = highest existing + 1
    repair_number = max([r["number"] for r in repairs], default=0) + 1

    client = input("Client name: ").strip()
    if not client:
        print("❌ Client name is required.")
        return

    device = input("Device: ").strip()
    if not device:
        print("❌ Device is required.")
        return

    problem = input("Problem: ").strip()

    amount_input = input("Amount charged (KSh): ").strip()
    try:
        amount = int(amount_input)
        if amount < 0:
            print("❌ Amount cannot be negative.")
            return
    except:
        print("❌ Amount must be a number.")
        return

    status = input("Status (fixed/pending/unfixable): ").strip().lower()
    if status not in ["fixed", "pending", "unfixable"]:
        print("❌ Status must be fixed, pending, or unfixable.")
        return

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    repair = {
        "number": repair_number,
        "date": now,
        "client": client,
        "device": device,
        "problem": problem,
        "amount": amount,
        "status": status
    }

    repairs.append(repair)
    save_repairs(repairs)

    print()
    print(f"✅ Repair #{repair_number} logged.")
    print()


def view_repairs():
    """View all repairs."""
    repairs = load_repairs()

    if not repairs:
        print("No repairs logged yet.")
        return

    print()
    print("=" * 60)
    print(f"   ALL REPAIRS ({len(repairs)} total)")
    print("=" * 60)

    for r in repairs:
        print(f"#{r['number']}  {r['date']}")
        print(f"     Client:  {r['client']}")
        print(f"     Device:  {r['device']}")
        print(f"     Problem: {r['problem']}")
        print(f"     Amount:  KSh {r['amount']}")
        print(f"     Status:  {r['status']}")
        print("-" * 60)
    print()


def show_stats():
    """Show statistics."""
    repairs = load_repairs()

    if not repairs:
        print("No repairs logged yet.")
        return

    total = len(repairs)
    income = sum(r["amount"] for r in repairs)
    fixed = sum(1 for r in repairs if r["status"] == "fixed")
    pending = sum(1 for r in repairs if r["status"] == "pending")
    unfixable = sum(1 for r in repairs if r["status"] == "unfixable")

    print()
    print("=" * 50)
    print("   REPAIR STATISTICS")
    print("=" * 50)
    print(f"Total repairs:    {total}")
    print(f"Total income:     KSh {income}")
    if total > 0:
        print(f"Average per job:  KSh {income // total}")
    print()
    print(f"  Fixed:      {fixed}")
    print(f"  Pending:    {pending}")
    print(f"  Unfixable:  {unfixable}")
    print("=" * 50)
    print()


def search_repairs():
    """Search repairs by client or device."""
    repairs = load_repairs()

    if not repairs:
        print("No repairs logged yet.")
        return

    keyword = input("Search by client or device: ").strip().lower()
    if not keyword:
        return

    results = [r for r in repairs if keyword in r["client"].lower() or keyword in r["device"].lower()]

    if not results:
        print("No matching repairs found.")
        return

    print()
    print(f"Found {len(results)} matching repair(s):")
    print("=" * 60)
    for r in results:
        print(f"#{r['number']}  {r['date']}  — {r['client']} ({r['device']})")
        print(f"     Problem: {r['problem']}  |  Amount: KSh {r['amount']}  |  Status: {r['status']}")
        print("-" * 60)
    print()


def generate_receipt():
    """Generate a receipt for a chosen repair."""
    repairs = load_repairs()

    if not repairs:
        print("No repairs logged yet.")
        return

    try:
        number = int(input("Enter repair number: "))
    except:
        print("Invalid number.")
        return

    repair = None
    for r in repairs:
        if r["number"] == number:
            repair = r
            break

    if not repair:
        print(f"No repair found with number #{number}.")
        return

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    receipt = f"""
{'=' * 50}
          FELIX TECH SERVICES
          Phone: 0712 XXX XXX
          Email: felixotieno1011@gmail.com
{'=' * 50}

Receipt Date:   {now}
Receipt #:      {repair['number']}
Original Date:  {repair['date']}
Client:         {repair['client']}
Device:         {repair['device']}

SERVICE DETAILS:
  Problem:      {repair['problem']}
  Status:       {repair['status']}

AMOUNT:         KSh {repair['amount']}

{'=' * 50}
  Thank you for your business!
{'=' * 50}
"""
    print(receipt)


def main():
    while True:
        print("=== Repair Log v2 ===")
        print("1. Add a repair")
        print("2. View all repairs")
        print("3. View statistics")
        print("4. Search repairs")
        print("5. Generate receipt")
        print("6. Exit")
        choice = input("Choice: ").strip()

        if choice == "1":
            add_repair()
        elif choice == "2":
            view_repairs()
        elif choice == "3":
            show_stats()
        elif choice == "4":
            search_repairs()
        elif choice == "5":
            generate_receipt()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
