#!/usr/bin/env python
from Tkinter import *
import os
import csv

#path to the csv file
policyFile = "firewallpolicies.csv"
#path to create a test file
newPolicyFile = "newFirewall.csv"

#lists of initial rules
entries1 = []
entries2 = []

#lists of the instances of all entries
listEntries1 = []
listEntries2 = []

#lists of final rules (when user clics on "save")
entriesFinal1 = []
entriesFinal2 = []


#Creates the initial widgets
def createWidgets(root):
	
	window1.grid(row=0, column=0)
	#frame for 2nd set of entries
	
	window2.grid(row=0, column=1)
	#for each rule (1st IP)
	for field in entries1:
		#Creates a new row
		row = Frame(window1)
		lab = Label(row, text='Rule '+str(len(listEntries1)+1), anchor='w')
		ent1 = Entry(row)
		#insert the correponding rile in the entry
		ent1.insert(0, field)
		listEntries1.append(ent1)
		row.pack(side=TOP, padx=5, pady=5)
		lab.pack(side=LEFT)
		ent1.pack(side=LEFT)
		
		#for each rule (2nd IP)
	for field in entries2:
		row2 = Frame(window2)
		ent2 = Entry(row2)
		ent2.insert(0, field)
		photo=PhotoImage(file="Cross.gif")
		buttonDelete = Button(row2, text='Delete', command=root.quit)
		buttonDelete.config(image=photo, width=15, height=15)
		buttonDelete.image = photo
		listEntries2.append(ent2)
		row2.pack(side=TOP, fill=X, padx=5, pady=5)
		ent2.pack(side=LEFT)
		buttonDelete.pack(side=LEFT)


#get the different rules of the initial firewall
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


#get all actual rules displayed on the panel when the user click on the save button
def getEntries():
		del entriesFinal1[:]
		del entriesFinal2[:]
		for entry in listEntries1:
				entriesFinal1.append(entry.get())
		for entry in listEntries2:
				entriesFinal2.append(entry.get())
		#call function to update the csv file		
		writeInCSV()
		#label to indicate to the user that the rules are saved
		labSave = Label(root, text='Rules saved!', anchor='w')
		labSave.grid(row=1, column=0)
		root.after(1500, labSave.destroy)


#Updates the CSV file with the new ruser's rules
def writeInCSV():
		counting = 1
		csvTab = []
		#Creates a tab which is in the right format for csv file (id, IP1, IP2)
		for test in entriesFinal1:
				csvTab.append([str(counting), entriesFinal1[counting-1], entriesFinal2[counting-1]])
				counting+=1
		ifile = open(policyFile,"wb")
		output = csv.writer(ifile)
		for row in csvTab:
				output.writerow(row)
		ifile.close()	


def popUpNewRules():
		window = Toplevel(root)
		vcmd = (root.register(onValidate),
                '%P')
		labNewRules = Label(window, text='How many rules do you want to add?', anchor='w')
		entNumber = Entry(window, validate = 'key', validatecommand=vcmd)
		labNewRules.pack()
		entNumber.pack()
		buttonQuitAddRules = Button(window, text="Ok", command=lambda: quitAddRules(entNumber, window))
		buttonQuitAddRules.pack()



def onValidate(P):
	if isinstance(P, str):
		if (str.isdigit(P) or P == ""):
			return True
		else:
			return False
	else:
		return False		


def quitAddRules(entNumber, window):
	rulesToAddString = entNumber.get()
	if (rulesToAddString != ""):
		rulesToAdd = int(rulesToAddString)
		window.destroy()
		addRules(rulesToAdd)
	else:
		labWarning = Label(window, text='Please enter a number of new rules', anchor='w')
		labWarning.pack()
		window.after(1500, labWarning.destroy)


def addRules(rulesToAdd):
	for i in range(rulesToAdd):
		#1st column
		row = Frame(window1)
		lab = Label(row, text='Rule '+str(len(listEntries1)+1), anchor='w')
		ent1 = Entry(row)
		ent1.insert(0, '10.0.0.X')
		listEntries1.append(ent1)
		row.pack(side=TOP, fill=X, padx=5, pady=5)
		lab.pack(side=LEFT)
		ent1.pack(side=LEFT)

		#2nd column
		row2 = Frame(window2)
		ent2 = Entry(row2)
		ent2.insert(0, '10.0.0.X')
		listEntries2.append(ent2)
		row2.pack(side=TOP, fill=X, padx=5, pady=5)
		ent2.pack(side=RIGHT, pady=1)
		


#launch when this python file is called directly
if __name__ == '__main__':
	 #Creates master frame
	 root = Tk()
	 root.title('Adninistrator panel')
	 window1 = Frame(root)
	 window2 = Frame(root)
	 getFirewall()
	 createWidgets(root)
	 buttonNewRule = Button(root, text="Add new rule", command=popUpNewRules)
	 buttonNewRule.grid(row=2, column=2)
	 #Creates save button
	 buttonSave = Button(root, text="Save", command=getEntries)
	 buttonSave.grid(row=2, column=0)
	 #Creates quit button
	 buttonQuit = Button(root, text='Quit', command=root.quit)
	 buttonQuit.grid(row=2, column=1)
	 #Keep the application running
	 root.mainloop()