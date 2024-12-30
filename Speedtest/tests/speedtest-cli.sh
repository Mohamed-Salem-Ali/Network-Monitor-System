#!/bin/bash

# Define the CSV file path
CSV_FILE="speedtest_data.csv"

# Define the header with the id and date columns manually (as the first row)
HEADER='"id","date","server name","server id","idle latency","idle jitter","packet loss","download","upload","download bytes","upload bytes","share url","download server count","download latency","download latency jitter","download latency low","download latency high","upload latency","upload latency jitter","upload latency low","upload latency high","idle latency low","idle latency high"'

# Get the current date and time
DATE=$(date +"%Y-%m-%d %H:%M:%S")

# Check if the CSV file exists
if [ -f "$CSV_FILE" ]; then
    # If the file exists, get the last ID and increment it
    LAST_ID=$(tail -n 1 "$CSV_FILE" | awk -F',' '{print $1}')
    ID=$((LAST_ID + 1))
else
    # If the file doesn't exist, create the file with the header manually
    echo "$HEADER" > "$CSV_FILE"
    ID=1
fi

# Run the speedtest command and capture the results
SPEEDTEST_RESULTS=$(speedtest -f csv)

# Format the result by adding the ID and current date at the beginning
RESULT="$ID, $DATE, $SPEEDTEST_RESULTS"

# Append the result to the CSV file (ensure each entry is on a new line)
echo "$RESULT" >> "$CSV_FILE"
