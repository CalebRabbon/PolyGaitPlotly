import datetime
import csv

with open('ministock.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)

    for line in csv_reader:
        print(line[2])


timestamp = datetime.datetime(1970, 1, 1, 0, 0, 0).timestamp()
print(timestamp)

timestamp = datetime.datetime(1970, 1, 1, 1, 0, 0).timestamp()
print("additional hour so + 3600")
print(timestamp)

timestamp = datetime.datetime(1970, 1, 1, 1, 1, 0).timestamp()
print("+60")
print(timestamp)

timestamp = datetime.datetime(1970, 1, 1, 1, 1, 1).timestamp()
print("+1")
print(timestamp)
#E20019C60906AAF1135D1AAA,4,2018-02-03,16:07:37,b1951afa
