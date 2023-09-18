# Add a column 'timed' to the data.csv 
# Last 45 entries should be marked True in the timed column, the rest, False

import csv

filename = '/Users/justinlee/Documents/projport/s9-quant/data.csv'

# Step 1: Read the CSV data
with open(filename, 'r') as file:
    reader = csv.reader(file)
    rows = list(reader)

# Step 2: Determine the index from which the rows should be marked as True
index_for_true = len(rows) - 45 if len(rows) > 45 else 0

# Step 3: Add the new "timed" column
header, *data = rows
header.append("timed")

for idx, row in enumerate(data, 1):  # Starting index from 1 to consider header
    if idx >= index_for_true:
        row.append("True")
    else:
        row.append("False")

# Step 4: Write the updated rows
with open('new_data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(rows)
