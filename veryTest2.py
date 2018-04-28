#!/usr/bin/env python
from Tkinter import *



if __name__ == '__main__':
   root = Tk()
   root.title('Adninistrator panel')
   
   buttonQuit = Button(root, text='Quit', command=root.quit)
   buttonQuit.grid(row=1, column=1)
   root.mainloop()