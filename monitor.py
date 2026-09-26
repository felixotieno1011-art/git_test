#!/usr/bin/env python3
# This line tells the system: run this file using Python 3

import subprocess      # lets Python run terminal commands like "ping"
import datetime        # lets Python get the current date and time
import re              # lets Python search text with patterns (regex)

def get_ping_avg(target):
    # Runs ping to a target and returns the average time in ms
    # target = "8.8.8.8" or "google.com"

    result = subprocess.run(
        ["ping", "-c", "5", target],   # the command to run
        capture_output=True,           # catch the output
        text=True                      # give it to us as text
    )

    output = result.stdout             # all the text ping printed

    # Find the line with "min/avg/max" and grab the average number
    match = re.search(r"min/avg/max/mdev = [\d.]+/([\d.]+)", output)

    if match:
        return float(match.group(1))   # the average, as a number
    else:
        return None                    # ping failed or no match

def log_result():
    # Runs ping tests and writes the result to the log file

    # Get the current date and time
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Ping both targets
    ping_8888 = get_ping_avg("8.8.8.8")         # ping the DNS server
    ping_google = get_ping_avg("google.com")    # ping google.com

    # Calculate the difference (DNS overhead)
    if ping_8888 and ping_google:
        difference = ping_google - ping_8888
    else:
        difference = None

    # Open the log file and add the entry
    with open("network_log.txt", "a") as f:      # "a" = append (add to end)
        f.write(f"===== {now} =====\n")
        f.write(f"Ping to 8.8.8.8: {ping_8888} ms avg\n")
        f.write(f"Ping to google.com: {ping_google} ms avg\n")
        f.write(f"Difference: {difference} ms (DNS overhead)\n")
        f.write("\n")                             # blank line between entries

    # Print what we just did
    print(f"Logged at {now}")
    print(f"  8.8.8.8: {ping_8888} ms")
    print(f"  google.com: {ping_google} ms")


# Run the log function when this script is called
if __name__ == "__main__":
    log_result()
