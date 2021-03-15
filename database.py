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

with open('people.csv') as csvfile:
    readcsv = csv.reader(csvfile, delimiter=',')

    def storeReadCSV(l=[]):
        for i in readcsv:
            l.append(i)
        return l

    conn = sqlite3.connect('people.db')

    c = conn.cursor()

    #ONLY to be executed ONCE when creating the table instance. Delete after****************#
    c.execute("""CREATE TABLE people( 
        Name    TEXT, 
        Title   TEXT,
        City    TEXT,
        State   TEXT,
        Region  TEXT
    )""")
    #*****************************#

    c.executemany("INSERT INTO people VALUES(?,?,?,?,?)",
                  copy.deepcopy(storeReadCSV()))

    print('Command executed successfully...')

    conn.commit()

    conn.close()
