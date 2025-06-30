import csv
import random

input_file = "keywords_flat_output.csv"
output_file = "sampled_300_rows.csv"
sample_size = 300

# Read all rows
with open(input_file, newline='', encoding="utf-8") as f:
    reader = list(csv.reader(f))
    header, rows = reader[0], reader[1:]

# Sample
sampled = random.sample(rows, min(sample_size, len(rows)))

# Write output
with open(output_file, "w", newline='', encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(sampled)
