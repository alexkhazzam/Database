import sqlite3
import csv
import json

editedLists = []

with open('people.csv') as csvfile:
    readcsv = csv.reader(csvfile, delimiter=',')

    with open('state_to_region.json') as f:
        data = json.load(f)

    def trimList(list):
        for i in range(0, len(list)):
            list[i] = list[i].strip()
        return list

    rPos = 4
    sPos = 3

    for l in readcsv:
        l = trimList(l)

        def regionExists(pos=3):
            return (l[pos] in data.keys())

        if (len(l) == 5):
            if (regionExists() and (l[rPos] == '')):
                l[rPos] = data[l[sPos]]
        else:
            print(l)
            while(len(l) != 5):
                l.append('NULL')
            for i in range(0, len(l)):
                if (regionExists(i)):
                    l[rPos] = data[l[i]]
                    l[sPos] = l[i]
                    l[i] = 'NULL'
                    break
                if (l[i] == ''):
                    l[i] = 'NULL'

        editedLists.append(l)


def writeToCSV():
    with open('people.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        for i in editedLists:
            csvwriter.writerow(i)
        writeToSQLite()


def writeToSQLite():
    conn = sqlite3.connect('people.db')

    c = conn.cursor()

    c.execute("""CREATE TABLE people(
        Id      INTEGER,
        Name    TEXT,
        Title   TEXT,
        City    TEXT,
        State   TEXT,
        Region  TEXT
    )""")

    c.execute("INSERT INTO people VALUES()")

    conn.commit()

    conn.close()
