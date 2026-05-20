import csv


with open("in.csv", newline='') as csvfile:
    firmReader= csv.reader(csvfile, delimiter=',')#, quoting=csv.QUOTE_NONNUMERIC)

    for row in firmReader:
        print (row)
        print (row[0])
        print (row[1])
        print (row[2])

        print (row[1]=='')
    
