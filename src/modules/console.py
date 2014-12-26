#-------------------------------------------------------------------------------
# Name:        ThreadSafeConsole
# Purpose:
#
# Author:      Fredrik Lundh
#
# Created:     13/02/2002
# Modified:    26/12/2014 - James Burke
#
# Copyright:   (c) Fredrik Lundh 2002
#-------------------------------------------------------------------------------

from Tkinter import *
import Queue
import hyperlink

class Console(Frame):
    def __init__(self, master, **options):
        Frame.__init__(self, master)

        scrollbar = Scrollbar(self)
        scrollbar.pack(side='right', fill='y')
        self.text = Text(self, wrap='word', yscrollcommand=scrollbar.set, **options)
        self.text.pack()
        self.text.config(state='disabled')
        self.link = hyperlink.Hyperlink(self.text)

        self.queue = Queue.Queue()
        self.update_me()
    def write(self, line, link=None):
        self.queue.put((line,link))
    def clear(self):
        self.queue.put((None, None))
    def update_me(self):
        try:
            while 1:
                line, link = self.queue.get_nowait()

                self.text.config(state='normal')
                if line is None:
                    self.text.delete(1.0, END)
                else:
                    self.text.insert(END, str(line), link)
                self.text.see(END)
                self.update_idletasks()
                self.text.config(state='disabled')
        except Queue.Empty:
            pass
        self.after(100, self.update_me)