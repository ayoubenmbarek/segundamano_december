import csv

with open('segundamanoanterior12-12.csv', "rb") as infile, open('sorted_segundamanoanterior12-12.csv', "wb") as outfile:
        r = csv.DictReader(infile,delimiter=',')
        w = csv.DictWriter(outfile, r.fieldnames, delimiter=';', quoting=csv.QUOTE_ALL)
        w.writeheader()
        for row in r:
            w.writerow(row)
