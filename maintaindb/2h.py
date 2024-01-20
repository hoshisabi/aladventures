import csv

left_file = "../_data/adventures.csv"
with open(left_file, 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        if row['Runtime'] == "2" and row['Tier'] == "2":
            print(row['Title'], row['Code'], row['Season'])
