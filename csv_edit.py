# Add a column 'timed' to the data.csv 
# Last 45 entries should be marked True in the timed column, the rest, False

import csv

filename = 'data.csv'

# Step 1: Read the CSV data
with open(filename, 'r') as file:
    reader = csv.reader(file)
    rows = list(reader)

#438, 482

# Step 3: Add the new "timed" column
header, *data = rows
header.append("key_strokes")

for idx, row in enumerate(data, 1):  # Starting index from 1 to consider header
    row.append("0.000")

# Step 4: Write the updated rows
with open('new_data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(rows)
