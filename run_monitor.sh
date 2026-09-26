#!/bin/bash
# run_monitor.sh
# Runs monitor.py 10 times with a short pause between runs.

for i in $(seq 1 10); do
    echo "===== Run $i of 10 ====="
    python monitor.py
    echo ""
    if [ $i -lt 10 ]; then
        echo "Waiting 10 seconds..."
        sleep 10
    fi
done

echo "Monitoring complete."
