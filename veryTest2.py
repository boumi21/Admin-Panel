#!/usr/bin/env python
from Tkinter import *
import os
import csv

policyFile = "firewallpolicies.csv"
newPolicyFile = "newFirewall.csv"
entries1 = []
entries2 = []
listEntries1 = []
listEntries2 = []
entriesFinal1 = []
entriesFinal2 = []


def createWidgets(root):
	counter = 1
	window1 = Frame(root)
	window1.grid(row=0, column=0)
	window2 = Frame(root)
	window2.grid(row=0, column=1)
	for field in entries1:
		row = Frame(window1)
		lab = Label(row, text='Rule '+str(counter), anchor='w')
		ent1 = Entry(row)
		ent1.insert(0, field)
		listEntries1.append(ent1)
		row.pack(side=TOP, fill=X, padx=5, pady=5)
		lab.pack(side=LEFT)
		ent1.pack(side=LEFT)
		counter+=1
	for field in entries2:
		row2 = Frame(window2)
		ent2 = Entry(row2)
		ent2.insert(0, field)
		listEntries2.append(ent2)
		row2.pack(side=TOP, fill=X, padx=5, pady=5)
		ent2.pack(side=RIGHT, pady=1)



def getFirewall():
		ifile  = open(policyFile, "rb")
		reader = csv.reader(ifile)
		rownum = 0
		for row in reader:
				colnum = 0
				for col in row:
						#print '%-8s: %s' % (header[colnum], col)
						colnum += 1
				entries1.append(row[1])
				entries2.append(row[2])
				rownum += 1
		ifile.close()



def getEntries():
		for entry in listEntries1:
				entriesFinal1.append(entry.get())
		for entry in listEntries2:
				entriesFinal2.append(entry.get())
		writeInCSV()
		labSave = Label(root, text='Rules saved!', anchor='w')
		labSave.grid(row=1, column=0)


def writeInCSV():
		counting = 1
		csvTab = []
		for test in entriesFinal1:
				csvTab.append([str(counting), entriesFinal1[counting-1], entriesFinal2[counting-1]])
				counting+=1
		ifile = open(newPolicyFile,"wb")
		output = csv.writer(ifile)
		for row in csvTab:
				output.writerow(row)
		ifile.close()				
		print csvTab
		print entriesFinal1[1]	



if __name__ == '__main__':
	 root = Tk()
	 root.title('Adninistrator panel')
	 getFirewall()
	 createWidgets(root)
	 buttonSave = Button(root, text="Save", command=getEntries)
	 buttonSave.grid(row=2, column=0)
	 buttonQuit = Button(root, text='Quit', command=root.quit)
	 buttonQuit.grid(row=2, column=1)
	 root.mainloop()