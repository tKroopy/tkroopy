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


if __name__ == '__main__':
    #import HyperlinkManager
    from Tkinter import *

    root = Tk()
    root.title("hyperlink-1")

    text = Text(root)
    text.pack()

    hyperlink = Hyperlink(text)

    def click1():
        print "click 1"

    text.insert(INSERT, "this is a ")
    text.insert(INSERT, "link", hyperlink.add(click1))
    text.insert(INSERT, "\n\n")

    def click2():
        print "click 2"

    text.insert(INSERT, "this is another ")
    text.insert(INSERT, "link", hyperlink.add(click2))
    text.insert(INSERT, "\n\n")

    mainloop()