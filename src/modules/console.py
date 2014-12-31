#-------------------------------------------------------------------------------
# Name:        Hyperlink Manager
# Purpose:
#
# Author:      Fredrik Lundh
#
# Created:     25/10/2000
# Copyright:   (c) Fredrik Lundh 2000
#-------------------------------------------------------------------------------

from Tkinter import *

class Hyperlink:

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

import Queue

class Console(Frame):
    def __init__(self, master, **options):
        Frame.__init__(self, master)

        scrollbar = Scrollbar(self)
        scrollbar.pack(side='right', fill='y')
        self.text = Text(self, wrap='word', yscrollcommand=scrollbar.set, **options)
        self.text.pack()
        self.text.config(state='disabled')
        self.link = Hyperlink(self.text)

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

if __name__ == '__main__':
    # testing application
    import time
    root = Tk()
    console = Console(root)
    console.pack()

    def count():
        for i in range(0, 10):
            console.write('%s\n' % i)
            time.sleep(0.1)

        def click1():
            print "click 1"

        console.write("this is a ")
        console.write("link", console.link.add(click1))
        console.write("\n\n")

    import threading
    t = threading.Thread(target=count)
    t.daemon = True
    t.start()

    root.mainloop()
    exit()