#!/usr/bin/env python
from Tkinter import *
import os
import csv

policyFile = "firewallpolicies.csv"
entries1 = []
entries2 = []






def getFirewall():
    ifile  = open(policyFile, "rb")
    reader = csv.reader(ifile)
    rownum = 0
    for row in reader:
        # Save header row.
        if rownum == 0:
            header = row
        else:
            colnum = 0
            for col in row:
                #print '%-8s: %s' % (header[colnum], col)
                colnum += 1
            entries1.append(row[1])
            entries2.append(row[2])
        rownum += 1
    ifile.close()



def getEntries():
	print ent1


if __name__ == '__main__':
   root = Tk()
   root.title('Adninistrator panel')
   getFirewall()
   buttonQuit = Button(root, text='Quit', command=root.quit)
   buttonQuit.grid(row=1, column=1)
   root.mainloop()