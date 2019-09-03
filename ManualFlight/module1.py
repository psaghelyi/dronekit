
"""
Simple script for take off and control with arrow keys
"""

from threading import Thread
from mavcomm import mavcomm
from controller import controller

#- Importing Tkinter: sudo apt-get install python-tk
import Tkinter as tk



class Demo1:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.button1 = tk.Button(self.frame, text = 'New Window', width = 25, command = self.new_window)
        self.button1.pack()
        self.frame.pack()
    def new_window(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = Demo2(self.newWindow)

class Demo2:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.quitButton = tk.Button(self.frame, text = 'Quit', width = 25, command = self.close_windows)
        self.quitButton.pack()
        self.frame.pack()
    def close_windows(self):
        self.master.destroy()



if __name__ == "__main__":
    
    mc = mavcomm('udp:0.0.0.0:14551')
    #mc = mavcomm('udp:25.22.42.122:14551')

    # starting command loop        
    t = Thread(target=mc.send_command)
    t.start()

    root = tk.Tk()
    root.geometry('200x100')
    app = Demo1(root)


    ctr = controller(mc)
    root.bind_all("<KeyPress>", ctr.keydown)
    root.bind_all("<KeyRelease>", ctr.keyup)
    
    root.mainloop()

    mc.stop = True
    t.join()
 
 