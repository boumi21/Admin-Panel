#!/usr/bin/env python
from Tkinter import *
import os
import csv
import re
import subprocess

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

#For checking when creating widgets (no duplicate)
global pressDelete


#Creates the initial widgets
def createWidgets(root, *argv):

	top.grid(columnspan = 2, row=0)
	w = Label(top, text="Firewall admninistration", fg='red', font=('Helvetica',16))
	w.pack()
	
	window1.grid(row=1, column=0)
	#frame for 2nd set of entries
	
	window2.grid(row=1, column=1)
	#for each rule (1st IP)


	#Check if the user pressed on the delete button
	if argv:
		if argv[0] == True:
			del listEntries1[:]
			del listEntries2[:]
			pressDelete = False

	for field in entries1:
		#Creates a new row
		row = Frame(window1)
		lab = Label(row, text='Rule '+str(len(listEntries1)+1), anchor='w')
		ent1 = Entry(row)
		#insert the correponding rule in the entry
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
		buttonDelete = Button(row2, text='Delete', command=lambda i=len(listEntries2): deleteRules(i))
		buttonDelete.config(image=photo, width=15, height=15)
		buttonDelete.image = photo
		listEntries2.append(ent2)
		row2.pack(side=TOP, fill=X, padx=5, pady=5)
		ent2.pack(side=LEFT)
		buttonDelete.pack(side=LEFT)


#get the different rules of the initial firewall
def getFirewall():
		del entries1[:]
		del entries2[:]
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
				if verifyEntries(entry.get()):			
					entriesFinal1.append(entry.get())
				else:
					failEntries()
					return	
		for entry in listEntries2:
				if verifyEntries(entry.get()):
					entriesFinal2.append(entry.get())
				else:
					failEntries()
					return	
		
		#call function to update the csv file		
		writeInCSV()
		#label to indicate to the user that the rules are saved
		labSave = Label(root, text='Rules saved!', anchor='w')
		labSave.grid(row=2, column=0)
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


#Pop up when user wants to add new rules
def popUpNewRules():
		window = Toplevel(root)
		#call the digit checker
		vcmd = (root.register(onValidate),
                '%P')
		labNewRules = Label(window, text='How many rules do you want to add?', anchor='w')
		entNumber = Entry(window, validate = 'key', validatecommand=vcmd)
		labNewRules.pack()
		entNumber.pack()
		buttonQuitAddRules = Button(window, text="Ok", command=lambda: quitAddRules(entNumber, window))
		buttonQuitAddRules.pack()


def popUpInfo():
	window = Toplevel(root)
	text = Text(window, height=2, width=55)
	text.pack()
	text.insert(END, "https://github.com/boumi21/Admin-Panel    |    2018")



# Digit checker
def onValidate(P):
	if isinstance(P, str):
		if (str.isdigit(P) or P == ""):
			return True
		else:
			return False
	else:
		return False		


#What to do when user press 'ok' on the pop up for new rules, check is the entry is empty
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



#Create as many widgets as the user wants
def addRules(rulesToAdd):
	for i in range(rulesToAdd):
		#1st column
		row = Frame(window1)
		lab = Label(row, text='Rule '+str(len(listEntries1)+1), anchor='w')
		ent1 = Entry(row)
		ent1.insert(0, '10.0.0.X')
		listEntries1.append(ent1)
		row.pack(side=TOP, padx=5, pady=5)
		lab.pack(side=LEFT)
		ent1.pack(side=LEFT)

		#2nd column
		row2 = Frame(window2)
		ent2 = Entry(row2)
		ent2.insert(0, '10.0.0.X')
		photo=PhotoImage(file="Cross.gif")
		buttonDelete = Button(row2, text='Delete', command=lambda i=len(listEntries2): deleteRules(i))
		buttonDelete.config(image=photo, width=15, height=15)
		buttonDelete.image = photo
		listEntries2.append(ent2)
		row2.pack(side=TOP, fill=X, padx=5, pady=5)
		ent2.pack(side=LEFT)
		buttonDelete.pack(side=LEFT)



#Method called when user clicks on a delete button
def deleteRules(ruleToDelete):
	global top
	global window1
	global window2
	del listEntries1[ruleToDelete]
	del listEntries2[ruleToDelete]
	pressDelete = True
	getEntries()
	getFirewall()
	top.destroy()
	window1.destroy()
	window2.destroy()
	top = Frame(root)
	window1 = Frame(root)
	window2 = Frame(root)
	createWidgets(root, pressDelete)


def verifyEntries(IP):
	return re.match(r"10\.0\.0\.[0-9]+", IP)

def failEntries():
	labFail = Label(root, text='At least one IP is not good!', anchor='w')
	labFail.grid(row=2, column=0)
	root.after(1500, labFail.destroy)

def activateFiewall():
	#print 'lol'
	subprocess.Popen(['./pox/pox.py','forwarding.l2_learning', 'openflow.discovery', 'openflow.spanning_tree', '--no-flood', '--hold-down', 'pox.misc.firewall'])


def desactivateFirewall():
	#print 'lol2'
	subprocess.Popen(['fuser', '-k', '6633/tcp'])


#launch when this python file is called directly
if __name__ == '__main__':
	 #Creates master frame
	 root = Tk()
	 root.title('Adninistrator panel')
	 top = Frame(root)
	 window1 = Frame(root)
	 window2 = Frame(root)
	 pressDelete = False
	 getFirewall()
	 createWidgets(root)
	 buttonInfo = Button(root, text="?", command=popUpInfo, padx=5)
	 buttonInfo.grid(row=3, column=0, sticky=W)
	 buttonNewRule = Button(root, text="Add new rule", command=popUpNewRules)
	 buttonNewRule.grid(row=3, column=1)
	 #Creates save button
	 buttonSave = Button(root, text="Save", command=getEntries)
	 buttonSave.grid(row=3, column=0)
	 #Creates quit button
	 buttonQuit = Button(root, text='Quit', command=root.quit)
	 buttonQuit.grid(row=3, column=2)
	 buttonStart = Button(root, text='Start', command=activateFiewall)
	 buttonStart.grid(row=3, column=3)
	 buttonStop = Button(root, text='Stop', command=desactivateFirewall)
	 buttonStop.grid(row=3, column=4)
	 #Keep the application running
	 root.mainloop()