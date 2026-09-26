#!/bin/bash
# Runs monitor.py 10 times, with a 5-minute pause between runs

for i in $(seq 1 10); do                    # loop 10 times (i = 1, 2, ... 10)
    echo "===== Run $i of 10 ====="          # show which run this is
    python monitor.py                        # run the monitor script
    echo ""                                  # blank line
    if [ $i -lt 10 ]; then                   # if not the last run...
        echo "Waiting 5 minutes..."          # tell the user
        sleep 5                            # wait 300 seconds (5 minutes)
    fi
done                                         # end of loop

echo "Monitoring complete. 10 runs finished."
