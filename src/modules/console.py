#-------------------------------------------------------------------------------
# Name:        Hyperlink Manager
# Purpose:
#
# Author:      Fredrik Lundh
#
# Created:     25/10/2000
#
# Copyright:   (c) Fredrik Lundh 2000
# Source:      http://effbot.org/zone/tkinter-text-hyperlink.htm
#-------------------------------------------------------------------------------

from Tkinter import *
import logging

log = logging.getLogger(__package__)

class Hyperlink(object):

    def __init__(self, text):

        self.text = text

        self.text.tag_config("hyper", foreground="blue", underline=1)

        self.text.tag_bind("hyper", "<Enter>", self._enter)
        self.text.tag_bind("hyper", "<Leave>", self._leave)
        self.text.tag_bind("hyper", "<Button-1>", self._click)

        self.reset()

    def reset(self):
        self.links = {}

    def add(self, action):
        # add an action to the manager.  returns tags to use in
        # associated text widget
        tag = "hyper-%d" % len(self.links)
        self.links[tag] = action
        return "hyper", tag

    def _enter(self, event):
        self.text.config(cursor="hand2")

    def _leave(self, event):
        self.text.config(cursor="")

    def _click(self, event):
        for tag in self.text.tag_names(CURRENT):
            if tag[:6] == "hyper-":
                self.links[tag]()
                return

#-------------------------------------------------------------------------------
# Name:        Console (originally named ThreadSafeConsole)
# Purpose:     Create a Text widget which can be output to in a thread
#
# Author:      Fredrik Lundh
#
# Created:     13/02/2002
# Modified:    26/12/2014 - James P Burke
#
# Copyright:   (c) Fredrik Lundh 2002
# Source:      http://effbot.org/zone/tkinter-threads.htm
#-------------------------------------------------------------------------------

import Queue

class Console(Frame):
    def __init__(self, master, **kwargs):
        Frame.__init__(self, master)

        scrollbar = Scrollbar(self)
        scrollbar.pack(side='right', fill='y')
        self.text = Text(self, wrap='word', yscrollcommand=scrollbar.set, **kwargs)
        self.text.pack()
        self.text.config(state='disabled')
        self.link = Hyperlink(self.text)

        self.sequence = ['-', '\\', '|', '/']
        self.load = False

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
                elif link and link[0] == 'hyper':
                    self.text.insert(END, str(line), link)
                elif link and link == 'loader':
                    self.load = True
                    self.text.delete(self.text.index("end-2c"))
                    self.text.insert(self.text.index("end-1c"), str(line))
                    #print self.text.index("end-1c"), str(line)
                else:
                    if self.load:
                        self.text.delete(self.text.index("end-2c"))
                        self.text.insert(self.text.index("end-1c"), str(line))
                    else:
                        self.text.insert(END, str(line))
                    self.load = False
                self.text.see(END)
                self.update_idletasks()
                self.text.config(state='disabled')
        except Queue.Empty:
            pass
        self.after(100, self.update_me)
        if self.load:
            self.queue.put((self.sequence[0], 'loader'))
            self.sequence.append(self.sequence.pop(0))

if __name__ == '__main__':
    # testing application
    import time
    root = Tk()
    console = Console(root)
    console.pack()

    def count():
        console.write('Loading World...', 'loader')
        console.write('\nLoading World...', 'loader')
        console.write('\nLoading World...', 'loader')
        time.sleep(3)
        console.write('Done')

        def click1():
            print "click 1"

        console.write("\nthis is a ")
        console.write("link", console.link.add(click1))
        console.write("\n\n")

    import threading
    t = threading.Thread(target=count)
    t.daemon = True
    t.start()

    root.mainloop()
    exit()