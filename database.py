import sqlite3
import csv
import json
import copy

editedLists = []


def trimList(list):
    for i in range(0, len(list)):
        list[i] = list[i].strip()
    return list


with open('people.csv') as csvfile:
    readcsv = csv.reader(csvfile, delimiter=',')

    with open('state_to_region.json') as f:
        data = json.load(f)

    rPos = 4
    sPos = 3

    elPos = 0
    for l in readcsv:
        l = trimList(l)

        def regionExists(pos=3):
            return (l[pos] in data.keys())

        if (len(l) == 5 and elPos != 0):
            if (regionExists() and (l[rPos] == '')):
                l[rPos] = data[l[sPos]]
        else:
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

        elPos += 1
        editedLists.append(l)

with open('people.csv', 'w') as csvfile:
    csvriter = csv.writer(csvfile)
    for i in editedLists:
        csvriter.writerow(i)

# Need to retrieve new people.csv file once "Region" section was populated and stored
with open('people.csv') as csvfile:
    readcsv = csv.reader(csvfile, delimiter=',')

    def fetchCSVItems():
        l = []
        k = 0
        for i in readcsv:
            if (k == 0):
                i.insert(0, "Id")
            else:
                i.insert(0, k)
            l.append(i)
            k += 1
        return l

    conn = sqlite3.connect('people.db')

    c = conn.cursor()

    #ONLY to be executed ONCE when creating the table instance. Delete after****************#
    c.execute("""CREATE TABLE people(
        Id      INTEGER,
        Name    VARCHAR,
        Title   VARCHAR,
        City    VARCHAR,
        State   VARCHAR,
        Region  VARCHAR
    )""")
    # *****************************

    c.executemany("INSERT INTO people VALUES(?,?,?,?,?,?)",
                  copy.deepcopy(fetchCSVItems()))  # Safer to not have a reference

    c.execute("SELECT * FROM people")

    items = c.fetchall()
    for item in items:
        print(item)

    conn.commit()

    conn.close()
