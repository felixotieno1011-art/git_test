#!/usr/bin/env python3
# report.py
# Reads the log file and shows a summary report.

import re


def read_numbers(pattern, filename):
    """Read a file and return all numbers that match a pattern."""
    numbers = []
    with open(filename, "r") as f:
        for line in f:
            match = re.search(pattern, line)
            if match:
                numbers.append(float(match.group(1)))
    return numbers


def show_stats(name, values):
    """Print average, best, and worst for a list of numbers."""
    if len(values) == 0:
        print(name, "— no data")
        return

    average = sum(values) / len(values)
    worst = max(values)
    best = min(values)

    print(name)
    print("  Tests:", len(values))
    print("  Average:", round(average, 1), "ms")
    print("  Best:", round(best, 1), "ms")
    print("  Worst:", round(worst, 1), "ms")


def main():
    logfile = "network_log.txt"

    # Find all ping numbers in the log
    ip_times = read_numbers(r"Ping to 8\.8\.8\.8: ([\d.]+) ms", logfile)
    domain_times = read_numbers(r"Ping to google\.com: ([\d.]+) ms", logfile)

    print("===== NETWORK HEALTH REPORT =====")
    print()

    show_stats("Ping to 8.8.8.8", ip_times)
    print()
    show_stats("Ping to google.com", domain_times)

    # DNS overhead
    if len(ip_times) > 0 and len(domain_times) > 0:
        avg_ip = sum(ip_times) / len(ip_times)
        avg_domain = sum(domain_times) / len(domain_times)
        overhead = avg_domain - avg_ip
        print()
        print("DNS overhead (avg):", round(overhead, 1), "ms")
        if overhead > 200:
            print("  → DNS is very slow")
        elif overhead > 100:
            print("  → DNS is slow")
        else:
            print("  → DNS is fine")


if __name__ == "__main__":
    main()
