#! /usr/bin/env python3

"""
MODULE DOCS
"""


from tkinter import *

class Dashboard(Frame):
    counter = 0

    def __init__(self, *args, **kwargs):
        
        Frame.__init__(self, *args, **kwargs)
        self.master.title("Zerg Mining")

        self.label = Label(self.master, text="Zerg Mining Dashboard")
        self.label.pack()

        self.map_button1 = Button(self.master, text="First Map", command=lambda: self.create_window("THIS IS DATA"))
        self.map_button1.pack()

        self.map_button2 = Button(self.master, text="Second Map", command=lambda: self.create_window("THIS IS alittle bit of DATA"))
        self.map_button2.pack()

        self.map_button3 = Button(self.master, text="Third Map", command=lambda: self.create_window("THIS IS SOME DATA!"))
        self.map_button3.pack()

        self.quit_button = Button(self.master, text="QUIT", command=quit)
        self.quit_button.pack()        
    
    def create_window(self, map_data):

        self.counter += 1
        # Would pass in the graph object string to print to the window
        t = Toplevel(self.master)
        t.wm_title("Map ID: {}".format(self.counter))
        output = Message(t, text=str(map_data), padx=10, pady=10, justify=RIGHT)
        output.pack()
        

if __name__  =="__main__":
    root = Tk()
    main = Dashboard(root)
    main.pack()
    root.mainloop()
