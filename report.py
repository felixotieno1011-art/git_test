#!/usr/bin/env python3
# The report script - reads the log and makes a summary

import re     # for finding numbers in the log

# The file we'll read
logfile = "network_log.txt"

# Lists to hold all the numbers we find
ping_8888_list = []      # will hold all 8.8.8.8 ping times
ping_google_list = []    # will hold all google.com ping times

# Open the log file and read it line by line
with open(logfile, "r") as f:          # "r" = read mode
    for line in f:                     # go through each line
        # Look for the "Ping to 8.8.8.8: NUMBER ms" line
        match_8888 = re.search(r"Ping to 8\.8\.8\.8: ([\d.]+) ms", line)
        if match_8888:
            ping_8888_list.append(float(match_8888.group(1)))

        # Look for the "Ping to google.com: NUMBER ms" line
        match_google = re.search(r"Ping to google\.com: ([\d.]+) ms", line)
        if match_google:
            ping_google_list.append(float(match_google.group(1)))

# Count how many tests we ran
total = len(ping_8888_list)

# Calculate statistics for 8.8.8.8
if total > 0:
    avg_8888 = sum(ping_8888_list) / total
    worst_8888 = max(ping_8888_list)
    best_8888 = min(ping_8888_list)
    avg_google = sum(ping_google_list) / total
    worst_google = max(ping_google_list)
    best_google = min(ping_google_list)
    dns_overhead = avg_google - avg_8888

    # Print the report
    print("===== NETWORK HEALTH REPORT =====")
    print(f"Total tests: {total}")
    print()
    print(f"Average ping to 8.8.8.8: {avg_8888:.1f} ms")
    print(f"Worst: {worst_8888:.0f} ms")
    print(f"Best: {best_8888:.0f} ms")
    print()
    print(f"Average ping to google.com: {avg_google:.1f} ms")
    print(f"Worst: {worst_google:.0f} ms")
    print(f"Best: {best_google:.0f} ms")
    print()
    print(f"DNS overhead (avg): {dns_overhead:.1f} ms")
    print("-> If this is high, DNS is slow")
else:
    print("No data yet. Run monitor.py first.")
