import csv
import re

right_file = "_data/DC-PoA List and Story Seeds Used - By Title.csv"
left_file = "_data/adventures.csv"
updated_file = "_data/adventures2.csv"
keys = ["Code", "Title", "Levels", "Runtime", "RelDate", "Season", "Authors", "Tier", "Price", "Seed", "G.Ad.","Eber","RMH", "Epic", "URL"]

adventure_details = {}

# affiliate_id=171040
def replace_affiliate(s):
    if "dmsguild.com" not in s:
        return s
    elif "affiliate_id=" in s:
        return re.sub(r"affiliate_id=\d+", "affiliate_id=171040", s)
    else:
        return f"{s}?affiliate_id=171040"

def make_key(s):
    s = re.sub(r"(DD(?:AL|EX))0(\d)-", r"\1\2", s)
    s = re.sub(r"\W", "", s)
    return s

with open(left_file, 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        adventure_details[make_key(row['Code'])] = row

with open(right_file, 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        key = make_key(row['DC Code'])
        if key in adventure_details:
            old_row = adventure_details[key]
        else:
            old_row = {'Code': row['DC Code'], 'Title': row['DC Name']}
        old_row["Seed"] = row["Seed Name"]
        old_row["Runtime"] = row["Runtime"]
        old_row["RelDate"] = row["Date Published"]
        adventure_details[key] = old_row

with open(updated_file, "w", encoding='UTF8', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=keys)
    writer.writeheader()
    for row in adventure_details.values():
        writer.writerow(row)

print(adventure_details)
