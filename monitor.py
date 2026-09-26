#!/usr/bin/env python3
# monitor.py
# Tests network speed and saves the results to a log file.

import subprocess   # to run ping commands
import datetime     # to get the date and time
import re           # to find numbers in text


def ping_time(target):
    """Run ping to a target and return the average time in ms."""
    # Run the ping command 5 times
    result = subprocess.run(
        ["ping", "-c", "5", target],
        capture_output=True,
        text=True
    )

    # Look for the line with the average time
    match = re.search(r"min/avg/max/mdev = [\d.]+/([\d.]+)", result.stdout)

    if match:
        return float(match.group(1))   # the average, as a number
    else:
        return None                    # ping failed


def main():
    # Get current date and time
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Test both targets
    ping_ip = ping_time("8.8.8.8")         # raw IP — no DNS needed
    ping_domain = ping_time("google.com")  # domain — needs DNS

    # Build the log entry
    with open("network_log.txt", "a") as log:
        log.write("===== " + now + " =====\n")

        if ping_ip is None:
            log.write("Ping to 8.8.8.8: FAILED\n")
        else:
            log.write("Ping to 8.8.8.8: " + str(ping_ip) + " ms\n")

        if ping_domain is None:
            log.write("Ping to google.com: FAILED\n")
        else:
            log.write("Ping to google.com: " + str(ping_domain) + " ms\n")

        # Calculate DNS overhead if both succeeded
        if ping_ip is not None and ping_domain is not None:
            overhead = ping_domain - ping_ip
            log.write("DNS overhead: " + str(overhead) + " ms\n")

        log.write("\n")   # blank line between entries

    print("Logged at", now)
    print("  8.8.8.8:", ping_ip, "ms")
    print("  google.com:", ping_domain, "ms")


if __name__ == "__main__":
    main()
