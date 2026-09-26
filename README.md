# Network Health Monitor

## What it does
This project tests the network every few minutes and logs
the results. It records ping times to 8.8.8.8 and to
google.com. Then it makes a report showing the average,
best, and worst times, plus DNS overhead. This helps
find when and why the network is slow.

## Files
- monitor.py — tests the network and writes to the log
- report.py — reads the log and shows a summary
- run_monitor.sh — runs monitor.py 10 times with pauses
- network_log.txt — the saved test results
- analysis.txt — my findings and conclusions
- README.md — this file

## How to use
1. Run `python monitor.py` to test the network once
2. Run `./run_monitor.sh` to run 10 tests automatically
3. Run `python report.py` to see the summary report
4. Read `analysis.txt` for my conclusions

## What I learned
I learned how to use Python to run terminal commands
with subprocess. I learned how to read the output of
ping and find the average time. I learned how to save
data to a log file and read it back. I also learned
that DNS lookups can make websites slow even when the
basic connection is fine. Finally, I learned that
automating tests with a bash loop gives better data
than testing by hand.
