import csv

with open('names.csv', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        print row