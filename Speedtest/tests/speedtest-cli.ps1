# Define the CSV file path
$CSV_FILE = "speedtest_data.csv"

# Define the header with the id and date columns manually (as the first row)
$HEADER = '"id","date","server name","server id","idle latency","idle jitter","packet loss","download","upload","download bytes","upload bytes","share url","download server count","download latency","download latency jitter","download latency low","download latency high","upload latency","upload latency jitter","upload latency low","upload latency high","idle latency low","idle latency high"'

# Get the current date and time
$DATE = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

# Check if the CSV file exists
if (Test-Path $CSV_FILE) {
    # If the file exists, get the last ID and increment it
    $LAST_ENTRY = Get-Content $CSV_FILE | Select-Object -Last 1
    $LAST_ID = ($LAST_ENTRY -split ",")[0]  # Extract the ID from the last line
    $ID = [int]$LAST_ID + 1  # Increment the ID
    # Run the speedtest command without the --output-header flag
    $SPEEDTEST_RESULTS = speedtest -f csv 
}
else {
    # If the file doesn't exist, create the file with the header manually
    $HEADER | Out-File -FilePath $CSV_FILE -Encoding UTF8

    # Set the ID to 1 as this is the first entry
    $ID = 1
    # Run the speedtest command without the --output-header flag
    $SPEEDTEST_RESULTS = speedtest -f csv 
}

# Format the result by adding the ID and current date at the beginning
$RESULT = "$ID, $DATE, $SPEEDTEST_RESULTS"

# Append the result to the CSV file (ensure each entry is on a new line)
$RESULT | Out-File -FilePath $CSV_FILE -Append -Encoding UTF8
